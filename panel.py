import httpx
from config import PANEL_URL, PANEL_USERNAME, PANEL_PASSWORD, PANEL_TOKEN

class PanelError(Exception): pass

class PasarGuard:
    def __init__(self):
        self.base=PANEL_URL
        self.token=PANEL_TOKEN
        self.client=httpx.AsyncClient(timeout=25, follow_redirects=True)

    async def close(self): await self.client.aclose()

    async def login(self):
        if self.token: return self.token
        if not (self.base and PANEL_USERNAME and PANEL_PASSWORD): raise PanelError('Panel credentials are not configured.')
        # PasarGuard uses bearer JWT authentication. Try the standard OAuth2 form endpoint.
        for path in ('/api/token','/api/auth/token','/token'):
            try:
                r=await self.client.post(self.base+path,data={'username':PANEL_USERNAME,'password':PANEL_PASSWORD})
                if r.is_success:
                    data=r.json(); tok=data.get('access_token') or data.get('token')
                    if tok: self.token=tok; return tok
            except Exception: pass
        raise PanelError('Could not authenticate to PasarGuard. Put a valid PANEL_TOKEN in .env.')

    async def request(self, method, path, **kwargs):
        token=await self.login()
        headers=kwargs.pop('headers',{})
        headers['Authorization']='Bearer '+token
        r=await self.client.request(method,self.base+path,headers=headers,**kwargs)
        if r.status_code >= 400:
            raise PanelError(f'HTTP {r.status_code}: {r.text[:500]}')
        try: return r.json()
        except Exception: return {'raw':r.text}

    async def create_from_template(self, template_id, username, note=''):
        return await self.request('POST','/api/user/from_template',json={'user_template_id':template_id,'username':username,'note':note})

    async def bulk_from_template(self, template_id, count, strategy='random', username=None, start_number=None, note=''):
        body={'user_template_id':template_id,'count':count,'strategy':strategy,'username':username,'note':note}
        if start_number is not None: body['start_number']=start_number
        return await self.request('POST','/api/users/bulk/from_template',json=body)

    async def get_user(self, username):
        return await self.request('GET',f'/api/user/{username}')

    async def delete_user(self, username):
        return await self.request('DELETE',f'/api/user/{username}')

    async def update_user(self, username, payload):
        return await self.request('PUT',f'/api/user/{username}',json=payload)

    async def templates(self): return await self.request('GET','/api/user_template')
    async def nodes(self): return await self.request('GET','/api/node')
