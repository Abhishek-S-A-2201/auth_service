from sqlalchemy import Column, Integer, String, Boolean, JSON, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organization.id",
                    ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey(
        "role.id", ondelete="CASCADE"), nullable=False)
    status = Column(Integer, default=0, nullable=False)
    settings = Column(JSON, default={}, nullable=True)
    created_at = Column(BigInteger, nullable=True)
    updated_at = Column(BigInteger, nullable=True)
    organization = relationship("Organization", back_populates="members")
    user = relationship("User", back_populates="members")
    role = relationship("Role", back_populates="members")
