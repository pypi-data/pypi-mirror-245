from .template import TemplateResponse

from typing import Optional, Dict, Any

_template = TemplateResponse()

async def render(
    request,
    template_name: str,
    context: Dict[str, Any] = None,
    status_code: int = 200,
    headers: Dict[str, str] = None,
    inherit: Optional[str] = None
) -> TemplateResponse:
    try:
        return await _template(
            request,
            template_name,
            context,
            status_code,
            headers,
            inherit
        )
    except Exception as e:
        raise e