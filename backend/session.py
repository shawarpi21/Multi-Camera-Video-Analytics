from fastapi import Request, HTTPException
import logging

def require_login(request: Request):
    user = request.session.get("user")  # Check session instead of cookie
    if not user:
        logging.info("No user in session.")
        raise HTTPException(status_code=401, detail="Authentication required")
    return user  # Return the username for use in routes if needed