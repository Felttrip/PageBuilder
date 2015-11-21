from models.element import Element
from models.element_type import ElementType

class ElementDao(object):

    @staticmethod
    def get_elements_by_page(page_id):
        return Element.query.filter_by(page_id=page_id).all()

    @staticmethod
    def add_element(type, page_id, order,content):
        el_type = ElementType.query.filter_by(name=type).first()
        new_el = Element(el_type.id,page_id,order,content)
        Element.session.add(new_el)
        Element.session.commit()
        return


    @staticmethod
    def delete_elements(page_id):
        Element.query.filter_by(page_id=page_id).delete()
        Element.session.commit()
        return