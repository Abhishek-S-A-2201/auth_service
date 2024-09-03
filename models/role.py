from sqlalchemy import Column, Integer, String, Boolean, JSON, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    org_id = Column(Integer, ForeignKey("organization.id",
                    ondelete="CASCADE"), nullable=False)
    members = relationship("Member", back_populates="role")
    organization = relationship("Organization", back_populates="roles")
