from models.page import Page
from dao.elementdao import ElementDao


class PageDao(object):

    @staticmethod
    def get_page(page_id):
        page = Page.query.get(page_id)
        return page

    @staticmethod
    def get_pages_by_site(site_id):
        return Page.query.filter_by(site_id=site_id).order_by(Page.order).all()

    @staticmethod
    def add_page(name, site_id, order):
        new_page = Page(name,site_id, order)
        Page.session.add(new_page)
        Page.session.commit()
        return new_page

    @staticmethod
    def delete_page(page_id):
        Page.query.filter_by(id=page_id).delete()
        Page.session.commit()
        return

    @staticmethod
    def update_page(name, page_id, order):
        page = Page.query.get(page_id)
        page.name = name
        page.order = order
        Page.session.add(page)
        Page.session.commit()
        page = Page.query.get(page_id)
        return page
