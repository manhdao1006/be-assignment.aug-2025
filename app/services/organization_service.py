from app.repositories.organization_repository import OrganizationRepository
from app.models.organization import Organization

class OrganizationService:
    def __init__(self, org_repo: OrganizationRepository):
        self.org_repo = org_repo

    def get_all(self, skip: int = 0, limit: int = 10, sort_by: str = "id", sort_order: str = "asc"):
        if not hasattr(Organization, sort_by):
            sort_by = "id"
        column = getattr(Organization, sort_by)
        order_by = column.desc() if sort_order == "desc" else column.asc()
        organizations = self.org_repo.get_all(skip=skip, limit=limit, order_by=order_by)
        total = self.org_repo.count()
        pagination = {
            "total": total,
            "skip": skip,
            "limit": limit,
            "returned": len(organizations)
        }
        return {"pagination": pagination, "organizations": organizations}

    def get_by_id(self, org_id: int):
        org = self.org_repo.get_by_id(org_id)
        if not org:
            raise ValueError("Organization not found")
        return org

    def create(self, org_in):
        org = Organization(name=org_in.name)
        return self.org_repo.create(org)

    def update(self, org_id: int, org_in):
        org = self.org_repo.get_by_id(org_id)
        if not org:
            raise ValueError("Organization not found")
        org.name = org_in.name
        return self.org_repo.update(org)

    def soft_delete(self, org_id: int):
        org = self.org_repo.get_by_id(org_id)
        if not org:
            raise ValueError("Organization not found")
        return self.org_repo.soft_delete(org)
