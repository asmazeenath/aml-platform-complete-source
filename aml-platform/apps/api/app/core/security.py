# Production deployment must replace this development placeholder with verified JWT/OIDC auth.
from fastapi import Header, HTTPException
def require_role(*allowed):
    def dependency(x_demo_role: str = Header(default="analyst")):
        if x_demo_role not in allowed:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return x_demo_role
    return dependency
