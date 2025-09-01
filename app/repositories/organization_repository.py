from sqlalchemy.orm import Session
from app.models.organization import Organization

class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 10, order_by=None):
        query = self.db.query(Organization).filter(Organization.is_deleted == False)
        if order_by is not None:
            query = query.order_by(order_by)
        return query.offset(skip).limit(limit).all()

    def count(self):
        return self.db.query(Organization).filter(Organization.is_deleted == False).count()

    def get_by_id(self, org_id: int):
        return self.db.query(Organization).filter(Organization.id == org_id, Organization.is_deleted == False).first()

    def create(self, org: Organization):
        self.db.add(org)
        self.db.commit()
        self.db.refresh(org)
        return org

    def update(self, org: Organization):
        self.db.commit()
        self.db.refresh(org)
        return org

    def soft_delete(self, org: Organization):
        org.is_deleted = True
        self.db.commit()
        self.db.refresh(org)
        return org
