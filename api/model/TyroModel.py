# coding: utf-8
import decimal
import uuid
import sqlalchemy
from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, Integer, LargeBinary, SmallInteger, Unicode, text, \
    or_, and_, desc
from sqlalchemy.dialects.mssql import BIT, MONEY
from sqlalchemy.orm import relationship
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.sql import func
from sqlalchemy_pagination import paginate
from database import Base, flaskConfig

class SplitPayment(Base):
    __tablename__ = 'SplitPayment'

    uuid = Column(Unicode(40), primary_key=True)
    salesorder_id = Column(Integer, nullable=False)
    rrn = Column(Unicode(40), nullable=False)
    mid = Column(Unicode(20))
    tid = Column(Unicode(15))
    transaction_reference = Column(Unicode(40))
    table_code = Column(Unicode(15))
    staff_id = Column(Integer)
    amount = Column(MONEY, nullable=False, server_default=text("(0)"))
    surcharge_amount = Column(MONEY, nullable=False, server_default=text("(0)"))
    tip_amount = Column(MONEY, nullable=False, server_default=text("(0)"))
    transaction_amount = Column(MONEY, nullable=False, server_default=text("(0)"))
    card_currency = Column(Unicode(15))
    card_type = Column(Unicode(40))
    date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    drawer = Column(Unicode(1), nullable=False, index=True)

    @classmethod
    def getBySalesorderId(cls, salesorderId):
        res = cls.query.filter(cls.salesorder_id == salesorderId).all()
        return res

    @classmethod
    def checkDuplicate(cls, salesorderId, rrn):
        res = cls.query.filter(cls.salesorder_id == salesorderId, cls.rrn == rrn).first()
        return res

    @classmethod
    def insertSplitPayments(cls, salesorderId, rrn, mid, tid, transactionReference, tableCode, staffId,
                            baseAmount, surchargeAmount, tipAmount, transactionAmount, cardCurrency,
                            cardType, date, drawer):
        splitPayment = SplitPayment(uuid=uuid.uuid1().hex,
                                    salesorder_id=salesorderId,
                                    rrn=rrn,
                                    mid=mid,
                                    tid=tid,
                                    transaction_reference = transactionReference,
                                    table_code = tableCode,
                                    staff_id = staffId,
                                    amount = baseAmount,
                                    surcharge_amount = surchargeAmount,
                                    tip_amount=tipAmount,
                                    transaction_amount = transactionAmount,
                                    card_currency = cardCurrency,
                                    card_type = cardType,
                                    date=date,
                                    drawer=drawer)
        cls.query.session.add(splitPayment)
        cls.query.session.flush()
        # cls.query.session.commit()