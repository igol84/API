from fastapi import APIRouter, Depends, status, Response

from .. import crud

router = APIRouter(tags=['Json'], prefix='/json')  #


class XmlResponse(Response):
    media_type = "application/xml"

    def render(self, content: str) -> bytes:
        return content.encode("utf-8")


@router.get('/prom.xml', status_code=status.HTTP_201_CREATED)
def create_xml(crud_xml: crud.Xml = Depends()):
    return XmlResponse(crud_xml.create_xml())
