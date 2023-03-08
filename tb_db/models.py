from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import JSON
from sqlalchemy import event
from sqlalchemy import func
from sqlalchemy.orm import attributes
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.orm import relationship
from sqlalchemy.orm import make_transient
from sqlalchemy.orm import Session
from sqlalchemy import Table

def camel_to_snake(s: str) -> str:
    """
    Converts camelCase to snake_case
    :param s: String to convert
    :type s: str
    :return: snake_case equivalent of camelCase input
    :rtype: str
    """
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


class Base:
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)

association_table_cgmlst = Table(
    "association_table_cgmlst",
    Base.metadata,
    Column("sample_id", ForeignKey("sample.id")),
    Column("cgmlst_cluster_id", ForeignKey("cgmlst_cluster.id")),
)

association_table_miru = Table(
    "association_table_miru",
    Base.metadata,
    Column("sample_id", ForeignKey("sample.id"), primary_key=True),
    Column("miru_cluster_id", ForeignKey("miru_cluster.id"), primary_key=True),
)


class Sample(Base):

    sample_id = Column(String)
    accession = Column(String)
    collection_date = Column(Date)

    cgmlst_cluster = relationship("CgmlstCluster", secondary=association_table_cgmlst, backref = 'samples')
    miru_cluster = relationship("MiruCluster", secondary=association_table_miru, backref='samples')


class Library(Base):
    """
    """

    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)
    sequencing_run_id = Column(String)
    library_id = Column(String)


class CgmlstScheme(Base):
    """
    """

    name = Column(String)
    version = Column(String)
    num_loci = Column(Integer)


class CgmlstAlleleProfile(Base):
    """
    """

    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)
    cgmlst_scheme_id = Column(Integer, ForeignKey("cgmlst_scheme.id"), nullable=True)
    percent_called = Column(Float)
    profile = Column(JSON)


class MiruProfile(Base):
    """
    """

    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)
    percent_called = Column(Float)
    profile_by_position = Column(JSON)
    miru_pattern = Column(String)


class CgmlstCluster(Base):

    cluster_id = Column(String)


class MiruCluster(Base):

    cluster_id = Column(String)
