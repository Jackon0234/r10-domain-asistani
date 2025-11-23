import whois
import asyncio
import random
from datetime import datetime

class DomainChecker:
    def normalize_date(self, date_obj):
        if date_obj is None:
            return None
        
        if isinstance(date_obj, list):
            date_obj = date_obj[0]
            
        if isinstance(date_obj, str):
            try:
                return datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S')
            except:
                return None

        if hasattr(date_obj, 'replace'):
            return date_obj.replace(tzinfo=None)
            
        return date_obj

    def format_date_str(self, date_obj):
        dt = self.normalize_date(date_obj)
        if dt:
            return dt.strftime('%d.%m.%Y')
        return "Bilinmiyor"

    def calculate_days(self, creation_date, expiration_date):
        try:
            c_date = self.normalize_date(creation_date)
            e_date = self.normalize_date(expiration_date)
            now = datetime.now()
            
            if not c_date or not e_date:
                return "Hesaplanamadı", 0

            age_delta = now - c_date
            age_years = age_delta.days // 365
            age_months = (age_delta.days % 365) // 30
            
            domain_age = f"{age_years} Yıl"
            if age_months > 0:
                domain_age += f", {age_months} Ay"

            remaining_delta = e_date - now
            remaining_days = remaining_delta.days
            
            return domain_age, remaining_days
        except Exception:
            return "Hesaplanamadı", 0

    async def check(self, domain: str) -> dict:
        clean_domain = domain.lower().strip().replace("https://", "").replace("http://", "").replace("www.", "")
        
        if "." not in clean_domain:
            return {'status': 'error', 'message': 'Geçersiz uzantı.', 'domain': clean_domain}

        try:
            w = await asyncio.to_thread(whois.whois, clean_domain)
            
            if w.status is None and w.domain_name is None:
                 return {'status': 'available', 'domain': clean_domain}
            
            if w.creation_date or w.expiration_date:
                age, remaining = self.calculate_days(w.creation_date, w.expiration_date)
                
                clean_data = {
                    'registrar': w.registrar,
                    'creation_date': self.format_date_str(w.creation_date),
                    'expiration_date': self.format_date_str(w.expiration_date),
                    'name_servers': w.name_servers,
                    'emails': w.emails
                }

                return {
                    'status': 'registered', 
                    'domain': clean_domain, 
                    'data': clean_data,
                    'age': age,
                    'remaining_days': remaining
                }
            
            return {'status': 'available', 'domain': clean_domain}

        except Exception as e:
            error_msg = str(e).lower()
            if "no match" in error_msg or "not found" in error_msg:
                 return {'status': 'available', 'domain': clean_domain}
            
            return {'status': 'error', 'message': str(e), 'domain': clean_domain}

    async def get_smart_suggestions(self, domain: str) -> list:
        base = domain.split('.')[0]
        try: ext = domain.split('.')[-1]
        except: ext = "com"
            
        prefixes = ["get", "go", "my", "the", "try", "pro", "best", "super", "net", "web"]
        suffixes = ["app", "shop", "store", "tech", "hub", "online", "blog", "tr"]
        
        candidates = []
        for p in random.sample(prefixes, 2):
            candidates.append(f"{p}{base}.{ext}")
        for s in random.sample(suffixes, 2):
            candidates.append(f"{base}{s}.{ext}")
            
        available_suggestions = []
        for cand in candidates:
            res = await self.check(cand)
            if res['status'] == 'available':
                available_suggestions.append(cand)
        return available_suggestions