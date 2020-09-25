# coding: utf-8
import decimal
import uuid
import sqlalchemy
from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, Integer, LargeBinary, SmallInteger, Unicode, text, \
    or_, and_
from sqlalchemy.dialects.mssql import BIT, MONEY
from sqlalchemy.orm import relationship
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.sql import func
from sqlalchemy_pagination import paginate
from database import Base


class Tables(Base):
    __tablename__ = 'Tables'

    # column_not_exist_in_db = Column(Integer) # just add for sake of this error, dont add in db
    table_id = Column(Integer, nullable=False, primary_key=True)
    site_id = Column(Integer, nullable=False)
    table_code = Column(Unicode(15), nullable=False)
    table_status = Column(SmallInteger, nullable=False)
    seats = Column(SmallInteger, nullable=False)
    inactive = Column(BIT, nullable=False)
    staff_id = Column(Integer)
    logon_time = Column(DateTime)
    computer_user = Column(Unicode(100))
    start_time = Column(DateTime)
    ip = Column(Unicode(20))
    kb_id = Column(Integer)

    @classmethod
    def getTableAll(cls):
        return cls.query.filter(cls.inactive == 0).all()

    @classmethod
    def getTableByTableCode(cls, tableCode):
        return cls.query.filter(cls.table_code == tableCode).first()

    @classmethod
    def activateTable(cls, tableCode, time):
        return cls.query.filter(cls.table_code == tableCode).update(
            {"table_status": 2, "start_time": time, "staff_id": 0})

    @classmethod
    def deactivateTable(cls, tableCode):
        return cls.query.filter(cls.table_code == tableCode).update({"table_status": 0})


class Site(Base):
    __tablename__ = 'Site'
    site_id = Column(Integer, nullable=False, primary_key=True)
    site_code = Column(Unicode(15), nullable=False)
    site_name = Column(Unicode(20), nullable=False)
    site_name2 = Column(Unicode(20), nullable=False)
    inactive = Column(BIT, nullable=False)
    printer = Column(Unicode(60))
    printer2 = Column(Unicode(60))

    @classmethod
    def getSiteAll(cls):
        return cls.query.all()


class Keyboard(Base):
    __tablename__ = 'Keyboard'
    kb_id = Column(Integer, nullable=False, primary_key=True)
    kb_name = Column(Unicode(64), nullable=False)
    btn_page = Column(Integer, nullable=False)
    btn_left = Column(Integer, nullable=False)
    btn_top = Column(Integer, nullable=False)
    btn_width = Column(Integer, nullable=False)
    btn_height = Column(Integer, nullable=False)
    btn_forecolor = Column(Integer, nullable=False)
    btn_backcolor = Column(Integer, nullable=False)
    btn_fontname = Column(Unicode(64), nullable=False)
    btn_fontsize = Column(Integer, nullable=False)
    btn_showpic = Column(BIT, nullable=False)
    cat_cols = Column(SmallInteger)
    cat_height = Column(SmallInteger)
    kb_name2 = Column(Unicode(20))
    cat_rows = Column(SmallInteger)
    menu_type_id = Column(Integer)
    menu_type_limit = Column(Integer)

    @classmethod
    def getActivateKeyboard(cls):
        return cls.query.filter(cls.kb_name2 == 'online').first()

    @classmethod
    def getAll(cls):
        return cls.query.all()

    @classmethod
    def getById(cls, kbId):
        return cls.query.filter(cls.kb_id == kbId).first()


class KeyboardCat(Base):
    __tablename__ = 'KeyboardCat'
    cat_id = Column(Integer, nullable=False, primary_key=True)
    cat_name = Column(Unicode(64), nullable=False)
    kb_id = Column(Integer, nullable=False, primary_key=True)
    btn_page = Column(Integer, nullable=False)
    btn_left = Column(Integer, nullable=False)
    btn_top = Column(Integer, nullable=False)
    btn_width = Column(Integer, nullable=False)
    btn_height = Column(Integer, nullable=False)
    btn_forecolor = Column(Integer, nullable=False)
    btn_backcolor = Column(Integer, nullable=False)
    btn_fontname = Column(Unicode(64), nullable=False)
    btn_fontsize = Column(Integer, nullable=False)
    btn_showpic = Column(BIT, nullable=False)
    btn_rows = Column(SmallInteger)
    btn_cols = Column(SmallInteger)
    pic_align = Column(SmallInteger)
    text_align = Column(SmallInteger)
    invisible = Column(BIT)

    @classmethod
    def getActivateKeyboardCat(cls):
        try:
            res = cls.query.join(Keyboard, Keyboard.kb_id == cls.kb_id).filter(Keyboard.kb_name2 == 'online').order_by(
                cls.cat_id.asc()).all()
            return res
        except ProgrammingError:
            return None

    @classmethod
    def getByKbId(cls, kbId):
        query = cls.query.order_by(cls.kb_id.asc(), cls.cat_id.asc())
        if kbId:
            query = query.filter(cls.kb_id == kbId)

        res = query.all()
        return res

    @classmethod
    def getByCatIdAndKbId(cls, catId, kbId):
        res = cls.query.filter(cls.cat_id == catId, cls.kb_id == kbId).first()
        return res


class KeyboardItem(Base):
    __tablename__ = 'KeyboardItem'
    item_id = Column(Integer, nullable=False, primary_key=True)
    item_barcode = Column(Unicode(24), nullable=False)
    item_name = Column(Unicode(64), nullable=False)
    cat_id = Column(Integer, nullable=False, primary_key=True)
    kb_id = Column(Integer, nullable=False, primary_key=True)
    # btn_page = Column(Integer, nullable=False)
    # btn_left = Column(Integer, nullable=False)
    # btn_top = Column(Integer, nullable=False)
    # btn_width = Column(Integer, nullable=False)
    # btn_height = Column(Integer, nullable=False)
    # btn_forecolor = Column(Integer, nullable=False)
    btn_backcolor = Column(Integer, nullable=False)
    # btn_fontname = Column(Unicode(64), nullable=False)
    # btn_fontsize = Column(Integer, nullable=False)
    # btn_showpic = Column(BIT, nullable=False)
    # btn_showprice = Column(BIT)
    subcat_id = Column(Integer)
    stock_id = Column(Integer)
    subcat_link = Column(Unicode(999))

    @classmethod
    def getAvtiveKeyboardItem(cls, kbCatIds, kbId):
        res = cls.query.filter(cls.cat_id.in_(kbCatIds), cls.kb_id == kbId).order_by(cls.item_id.asc()).all()
        return res

    @classmethod
    def getByStockIdAndKbId(cls, stockId, kbId):
        res = cls.query.filter(cls.stock_id == stockId, cls.kb_id == kbId).first()
        return res

    @classmethod
    def getByBarcodeAndKbId(cls, barcode, kbId):
        res = cls.query.filter(cls.item_barcode == barcode, cls.kb_id == kbId).first()
        return res

    @classmethod
    def getByCatIdAndKbIdPagination(cls, kbId, catId, page, pageSize):
        query = cls.query.order_by(cls.item_id.desc())
        if kbId:
            query = query.filter(cls.kb_id == kbId)
        if catId:
            query = query.filter(cls.cat_id == catId)

        pagination = paginate(query, page, pageSize)

        return pagination

    @classmethod
    def getAllById(cls, kbId):
        res = cls.query.filter(cls.kb_id == kbId).order_by(cls.item_barcode.desc()).all()
        return res


class Category(Base):
    __tablename__ = 'Category'
    cat_id = Column(Integer, nullable=False, primary_key=True)
    cat_code = Column(Unicode(15), nullable=False)
    cat_name = Column(Unicode(40))
    cat_name2 = Column(Unicode(40), nullable=False)
    time_id = Column(Integer, nullable=False)
    printer = Column(Unicode(80))
    printer2 = Column(Unicode(80))
    inactive = Column(BIT, nullable=False)
    modifier1 = Column(Unicode(20))
    modifier2 = Column(Unicode(20))
    modifier3 = Column(Unicode(20))
    modifier4 = Column(Unicode(20))
    cat_name3 = Column(Unicode(40))
    cat_name4 = Column(Unicode(40))

    @classmethod
    def getByCatCode(cls, catCode):
        res = cls.query.filter(cls.cat_code == catCode).first()
        return res

    @classmethod
    def getByCatName(cls, catName):
        res = cls.query.filter(cls.cat_name == catName).first()
        return res


class Stock(Base):
    __tablename__ = 'Stock'
    __table_args__ = (
        Index('Sub', 'cat2', 'stock_id', unique=True),
        Index('Cat', 'cat1', 'stock_id', unique=True),
        Index('Bar code', 'barcode', 'stock_id', unique=True),
        Index('Supplier', 'supplier_id', 'stock_id', unique=True),
        Index('Custom1', 'custom1', 'stock_id', unique=True),
        Index('Categories', 'cat1', 'cat2', 'stock_id', unique=True),
        Index('Description', 'description', 'stock_id', unique=True),
        Index('Custom2', 'custom2', 'stock_id', unique=True)
    )

    stock_id = Column(Float(53), primary_key=True, server_default=text("(0)"))
    barcode = Column(Unicode(15), nullable=False, index=True)
    custom1 = Column(Unicode(50), nullable=False)
    custom2 = Column(Unicode(50), nullable=False)
    sales_prompt = Column(Unicode(100))
    inactive = Column(BIT, nullable=False, server_default=text("(0)"))
    allow_renaming = Column(BIT, nullable=False, server_default=text("(0)"))
    allow_fractions = Column(BIT, nullable=False, server_default=text("(0)"))
    package = Column(BIT, nullable=False, server_default=text("(0)"))
    tax_components = Column(BIT, nullable=False, server_default=text("(0)"))
    print_components = Column(BIT, nullable=False, server_default=text("(0)"))
    description = Column(Unicode(60), nullable=False)
    longdesc = Column(Unicode(255), nullable=False)
    cat1 = Column(Unicode(20), nullable=False)
    cat2 = Column(Unicode(20), nullable=False)
    goods_tax = Column(Unicode(3), nullable=False)
    cost = Column(MONEY, nullable=False, server_default=text("(0)"))
    sales_tax = Column(Unicode(3), nullable=False)
    sell = Column(MONEY, nullable=False, server_default=text("(0)"))
    quantity = Column(Float(53), nullable=False, server_default=text("(0)"))
    layby_qty = Column(Float(53), nullable=False, server_default=text("(0)"))
    salesorder_qty = Column(Float(53), nullable=False, server_default=text("(0)"))
    date_created = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    track_serial = Column(BIT, nullable=False, server_default=text("(0)"))
    static_quantity = Column(BIT, nullable=False, server_default=text("(0)"))
    bonus = Column(MONEY, nullable=False, server_default=text("(0)"))
    order_threshold = Column(Float(53), nullable=False, server_default=text("(0)"))
    order_quantity = Column(Float(53), nullable=False, server_default=text("(0)"))
    supplier_id = Column(ForeignKey('Supplier.supplier_id'), nullable=False, index=True, server_default=text("(0)"))
    date_modified = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    freight = Column(BIT, nullable=False, server_default=text("(0)"))
    use_scale = Column(BIT, nullable=False, server_default=text("(0)"))
    item_code = Column(Unicode(16), nullable=False)
    custom3 = Column(Unicode(50), nullable=False)
    custom4 = Column(Unicode(50), nullable=False)
    description2 = Column(Unicode(60), nullable=False)
    sell2 = Column(MONEY)
    sell3 = Column(MONEY)
    sell4 = Column(MONEY)
    show_extra = Column(BIT)
    show_taste = Column(BIT)
    show_qty = Column(BIT)
    cost2 = Column(MONEY)
    cost3 = Column(MONEY)
    cost4 = Column(MONEY)
    kitchen_desc = Column(Unicode(60))
    kitchen_desc2 = Column(Unicode(60))
    description3 = Column(Unicode(60))
    description4 = Column(Unicode(60))
    longdesc2 = Column(Unicode(255))
    longdesc3 = Column(Unicode(255))
    longdesc4 = Column(Unicode(255))

    # sell5 = Column(MONEY)
    # sell6 = Column(MONEY)
    # sell7 = Column(MONEY)
    # sell8 = Column(MONEY)

    # supplier = relationship('Supplier')

    @classmethod
    def getByStockId(cls, stockId):
        return cls.query.filter(cls.stock_id == stockId).one()

    @classmethod
    def getByBarcode(cls, barcode):
        return cls.query.filter(cls.barcode == barcode).first()

    @staticmethod
    def getPrice(stock, price):
        if stock.goods_tax == 'GST':
            return float(round(price * decimal.Decimal(1.1), 1))
        else:
            return float(round(price, 1))


class TasteStock(Base):
    __tablename__ = 'TasteStock'
    stock_id = Column(Integer, nullable=False, primary_key=True)
    taste_id = Column(Integer, nullable=False, primary_key=True)
    visible_type = Column(SmallInteger)

    @classmethod
    def getAll(cls):
        try:
            res = cls.query.filter(cls.visible_type == 1).order_by(cls.stock_id.desc()).all()
            return res
        except ProgrammingError:
            return []

    @classmethod
    def getByStockId(cls, stockId):
        try:
            res = cls.query.filter(cls.stock_id == stockId).filter(cls.visible_type == 1).all()
            return res
        except ProgrammingError:
            return []

    @classmethod
    def updateVisibleType(cls, stockId, tasteId, visibleType):
        res = cls.query.filter(cls.stock_id == stockId, cls.taste_id == tasteId).first()
        if res is not None:
            res.visible_type = visibleType
            cls.query.session.flush()
            cls.query.session.commit()


class ExtraStock(Base):
    __tablename__ = 'ExtraStock'
    stock_id = Column(Integer, nullable=False, primary_key=True)
    extra_id = Column(Integer, nullable=False, primary_key=True)
    visible_type = Column(SmallInteger)

    @classmethod
    def getAll(cls):
        try:
            res = cls.query.filter(cls.visible_type == 1).order_by(cls.stock_id.desc()).all()
            return res
        except ProgrammingError:
            return []

    @classmethod
    def getByStockId(cls, stockId):
        try:
            res = cls.query.filter(cls.stock_id == stockId).filter(cls.visible_type == 1).all()
            return res
        except ProgrammingError:
            return []

    @classmethod
    def updateVisibleType(cls, stockId, extraId, visibleType):
        res = cls.query.filter(cls.stock_id == stockId, cls.extra_id == extraId).first()
        if res is not None:
            res.visible_type = visibleType
            cls.query.session.flush()
            cls.query.session.commit()


class Staff(Base):
    __tablename__ = 'Staff'
    __table_args__ = (
        Index('Custom1', 'custom1', 'staff_id', unique=True),
        Index('Position', 'position', 'staff_id', unique=True),
        Index('Given Names', 'given_names', 'staff_id', unique=True),
        Index('Surname', 'surname', 'staff_id', unique=True),
        Index('Barcode', 'barcode', 'staff_id', unique=True),
        Index('Docket Name', 'docket_name', 'staff_id', unique=True),
        Index('State', 'state', 'staff_id', unique=True),
        Index('Custom2', 'custom2', 'staff_id', unique=True),
        Index('Suburb', 'suburb', 'staff_id', unique=True)
    )

    staff_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    barcode = Column(Unicode(15), nullable=False, unique=True)
    inactive = Column(BIT, nullable=False, server_default=text("(0)"))
    surname = Column(Unicode(50), nullable=False)
    given_names = Column(Unicode(50), nullable=False)
    docket_name = Column(Unicode(50), nullable=False)
    position = Column(Unicode(50), nullable=False)
    dob = Column(DateTime, nullable=False)
    commission = Column(Float(53), nullable=False, server_default=text("(0)"))
    addr1 = Column(Unicode(40), nullable=False)
    addr2 = Column(Unicode(40), nullable=False)
    addr3 = Column(Unicode(40), nullable=False)
    suburb = Column(Unicode(40), nullable=False)
    state = Column(Unicode(30), nullable=False)
    postcode = Column(Unicode(10), nullable=False)
    phone = Column(Unicode(20), nullable=False)
    mobile = Column(Unicode(20), nullable=False)
    email = Column(Unicode(50), nullable=False)
    custom1 = Column(Unicode(50), nullable=False)
    custom2 = Column(Unicode(50), nullable=False)
    status = Column(BIT, nullable=False, server_default=text("(0)"))
    date_modified = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))

    @classmethod
    def getStaffByBarcode(cls, barcode):
        return cls.query.filter(cls.barcode == barcode).first()

    @classmethod
    def getTyroSecret(cls):
        return cls.query.filter(cls.surname == 'Tyro').first()

    @classmethod
    def getPiselSecret(cls):
        return cls.query.filter(cls.surname == 'Pisel').first()


class RecordedDate(Base):
    __tablename__ = 'RecordedDate'
    date_type = Column(Integer, nullable=False, primary_key=True)
    date_modified = Column(DateTime, nullable=False)
    remark = Column(Unicode(50))

    @classmethod
    def get(cls, dateType):
        try:
            recordedDate = cls.query.filter(cls.date_type == dateType).one()
            return recordedDate
        except sqlalchemy.orm.exc.NoResultFound:
            return RecordedDate.insert(dateType, 0)

    @classmethod
    def insert(cls, dateType, dateModified):
        remark = ''
        if dateType == 1:
            remark = 'DocketOnline polling datetime'

        recordedDate = RecordedDate(date_type=dateType,
                                    date_modified=dateModified,
                                    remark=remark)

        cls.query.session.add(recordedDate)
        cls.query.session.flush()

        return recordedDate

    @classmethod
    def update(cls, dateType, dateModified):
        """更新记录时间"""
        recordedDate = cls.query.filter(cls.date_type == dateType).one()
        recordedDate.date_modified = dateModified
        cls.query.session.flush()
        return recordedDate.date_modified


class SaleID(Base):
    __tablename__ = 'SaleID'
    sale_type = Column(Integer, nullable=False, primary_key=True)
    sale_id = Column(Integer, nullable=False)
    date_modified = Column(DateTime, nullable=False)

    @classmethod
    def updateSalesorderId(cls):
        # FIXME can be null
        try:
            sale = cls.query.filter(cls.sale_type == 1).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return None

        sale.sale_id = sale.sale_id + 1
        cls.query.session.flush()
        # cls.query.session.commit()

        return sale.sale_id

    @classmethod
    def updateTakeawayId(cls):
        sale = cls.query.filter(cls.sale_type == 2).one()
        sale.sale_id = sale.sale_id + 1
        cls.query.session.flush()
        # cls.query.session.commit()

        return sale.sale_id


class Salesorder(Base):
    __tablename__ = 'SalesOrder'

    salesorder_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    salesorder_date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    expiry_date = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    staff_id = Column(ForeignKey('Staff.staff_id'), nullable=False, index=True, server_default=text("(0)"))
    customer_id = Column(ForeignKey('Customer.customer_id'), nullable=False, index=True, server_default=text("(0)"))
    transaction = Column(Unicode(2), nullable=False, index=True)
    original_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    custom = Column(Unicode(40))
    comments = Column(Unicode(255), nullable=False)
    subtotal = Column(MONEY, nullable=False, server_default=text("(0)"))
    discount = Column(MONEY, nullable=False, server_default=text("(0)"))
    rounding = Column(MONEY, nullable=False, server_default=text("(0)"))
    total_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    total_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    status = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    exported = Column(BIT, nullable=False, server_default=text("(0)"))
    guest_no = Column(SmallInteger)
    customer_name = Column(Unicode(40))

    customer = relationship('Customer')
    staff = relationship('Staff')

    @classmethod
    def insertSalesorder(cls, tableCode, guestNo, staffId, time, transaction, status):

        salesorderId = SaleID.updateSalesorderId()
        # if salesorderId is None:
        max = cls.query.session.query(func.max(cls.salesorder_id).label("max_id")).one()
        salesorderId = 1 if max.max_id is None else max.max_id + 1

        if transaction == 'TA':
            tableCode = 'TA' + '-OL-' + str(SaleID.updateTakeawayId())

        newSalesorder = Salesorder(salesorder_id=salesorderId,
                                   salesorder_date=time,
                                   expiry_date=time,
                                   staff_id=staffId,
                                   custom=tableCode,
                                   transaction=transaction,
                                   guest_no=guestNo,
                                   status=status,
                                   comments='')
        cls.query.session.add(newSalesorder)
        cls.query.session.flush()
        # cls.query.session.commit()

        return salesorderId, tableCode

    @classmethod
    def getSalesorderById(cls, id):
        try:
            salesorder = cls.query.filter(cls.salesorder_id == id).one()
            return salesorder
        except sqlalchemy.orm.exc.NoResultFound:
            return None

    @classmethod
    def getSalesorderByTableCode(cls, tableCode):
        return cls.query.filter(cls.custom == tableCode).order_by(cls.salesorder_date.desc()).first()

    @classmethod
    def getFirstOrderToday(cls, today):
        return cls.query.filter(cls.salesorder_date > today).order_by(cls.salesorder_date.asc()).first()

    @classmethod
    def updatePrice(cls, salesorderId):
        salesorder = cls.query.filter(cls.salesorder_id == salesorderId).one()
        salesOrderLines = SalesorderLine.query.filter(SalesorderLine.salesorder_id == salesorderId).all()
        if len(salesOrderLines) == 0:
            return

        salesorder.total_ex = decimal.Decimal(0)
        salesorder.total_inc = decimal.Decimal(0)

        for line in salesOrderLines:
            salesorder.total_ex += line.print_ex
            salesorder.total_inc += line.print_inc

        salesorder.subtotal = salesorder.total_inc

        return


class SalesorderOnline(Base):
    __tablename__ = 'SalesOrderOnline'

    uuid = Column(Unicode(40), primary_key=True)
    salesorder_id = Column(Integer, server_default=text("(0)"))
    actual_id = Column(Unicode(40))
    remark = Column(Unicode(40))
    status = Column(SmallInteger, nullable=False, server_default=text("(0)"))

    @classmethod
    def getActivateOrder(cls):
        return cls.query.filter(and_(cls.status != 11, cls.status != -1)).all()

    @classmethod
    def getBySalesorderId(cls, salesorderId):
        return cls.query.filter(cls.salesorder_id == salesorderId).first()

    @classmethod
    def insertSalesorderOnline(cls, salesorderId, actualId, remark, status):
        newSalesorderOnline = SalesorderOnline(uuid=uuid.uuid1().hex,
                                               salesorder_id=salesorderId,
                                               actual_id=actualId,
                                               remark=remark,
                                               status=status)
        cls.query.session.add(newSalesorderOnline)
        cls.query.session.flush()
        # cls.query.session.commit()

        return salesorderId


class SalesorderLine(Base):
    __tablename__ = 'SalesOrderLine'

    line_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    salesorder_id = Column(ForeignKey('SalesOrder.salesorder_id'), nullable=False, index=True,
                           server_default=text("(0)"))
    stock_id = Column(ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)"))
    cost_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    cost_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    sales_tax = Column(Unicode(3), nullable=False)
    sell_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    sell_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    rrp = Column(MONEY, nullable=False, server_default=text("(0)"))
    print_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    print_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    quantity = Column(Float(53), nullable=False, server_default=text("(0)"))
    parentline_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    package = Column(BIT, nullable=False, server_default=text("(0)"))
    status = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    orderline_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    size_level = Column(SmallInteger)
    staff_id = Column(Integer)
    time_ordered = Column(DateTime)
    out_order = Column(SmallInteger)
    hand_writting = Column(BIT)
    seq_id = Column(Integer)
    original_line_id = Column(Integer)

    salesorder = relationship('Salesorder')
    stock = relationship('Stock')

    @classmethod
    def get(cls, lineId):
        try:
            salesorderLine = cls.query.filter(cls.line_id == lineId).one()
            return salesorderLine
        except sqlalchemy.orm.exc.NoResultFound:
            return None

    @classmethod
    def getBySalesorderId(cls, salesorderId):
        return cls.query.filter(cls.salesorder_id == salesorderId).order_by(cls.line_id.asc()).all()

    @classmethod
    def getByOrderlineId(cls, orderlineId):
        return cls.query.filter(cls.orderline_id == orderlineId).order_by(cls.line_id.asc()).all()

    @classmethod
    def insertSalesorderLine(cls, salesorderId, stockId, sizeLevel, price, quantity, staffId, time, parentlineId,
                             status, orderlineId=None):
        max = cls.query.session.query(func.max(cls.line_id).label("max_id")).one()
        salesorderLineId = 1 if max.max_id is None else max.max_id + 1
        if orderlineId is None:
            orderlineId = salesorderLineId

        newSalesorderLine = SalesorderLine(line_id=salesorderLineId,
                                           salesorder_id=salesorderId,
                                           stock_id=stockId,
                                           sales_tax='GST',
                                           sell_ex=price / 1.1,
                                           sell_inc=price,
                                           rrp=price,
                                           print_ex=price / 1.1,
                                           print_inc=price,
                                           quantity=quantity,
                                           parentline_id=parentlineId,
                                           status=status,
                                           orderline_id=orderlineId,
                                           size_level=sizeLevel,
                                           staff_id=staffId,
                                           time_ordered=time)
        cls.query.session.add(newSalesorderLine)
        cls.query.session.flush()
        return salesorderLineId


class SalesorderLineOnline(Base):
    __tablename__ = 'SalesOrderLineOnline'

    uuid = Column(Unicode(40), primary_key=True)
    line_id = Column(Integer, server_default=text("(0)"))
    salesorder_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    actual_id = Column(Unicode(40))
    actual_line_id = Column(Unicode(40))
    stock_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    quantity = Column(Float(53), nullable=False, server_default=text("(0)"))
    size_level = Column(SmallInteger)
    status = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    type = Column(Unicode(40))

    @classmethod
    def getBySalesorderId(cls, salesorderId):
        return cls.query.filter(and_(cls.salesorder_id == salesorderId)).all()

    @classmethod
    def getLineId(cls, lineId, salesorderId):
        return cls.query.filter(and_(cls.line_id == lineId, cls.status != -1, cls.salesorder_id == salesorderId)).all()

    @classmethod
    def insertSalesorderLineOnline(cls, lineId, salesorderId, actualId, actualLineId, stockId, quantity, sizeLevel,
                                   status, type):
        newSalesorderLineOnline = SalesorderLineOnline(uuid=uuid.uuid1().hex,
                                                       line_id=lineId,
                                                       salesorder_id=salesorderId,
                                                       actual_id=actualId,
                                                       actual_line_id=actualLineId,
                                                       stock_id=stockId,
                                                       quantity=quantity,
                                                       size_level=sizeLevel,
                                                       status=status,
                                                       type=type)
        cls.query.session.add(newSalesorderLineOnline)
        cls.query.session.flush()
        return lineId


class Kitchen(Base):
    __tablename__ = 'Kitchen'
    line_id = Column(Integer, nullable=False, primary_key=True)
    orderline_id = Column(Integer, nullable=False, primary_key=True)
    table_code = Column(Unicode(40))
    staff_name = Column(Unicode(40), nullable=False)
    cat1 = Column(Unicode(40))
    description = Column(Unicode(60))
    description2 = Column(Unicode(60))
    unit = Column(Unicode(30))
    quantity = Column(Float(24), nullable=False)
    printer = Column(Unicode(100))
    printer2 = Column(Unicode(100))
    order_time = Column(DateTime, nullable=False)
    handwritting = Column(BIT, nullable=False)
    comments = Column(Unicode(200))
    stock_type = Column(SmallInteger)
    out_order = Column(SmallInteger)
    customer_name = Column(Unicode(40))
    cat2 = Column(Unicode(40))
    salesorder_id = Column(Integer)
    status = Column(SmallInteger)
    original_line_id = Column(Integer)

    @classmethod
    def getByLineId(cls, lineId):
        return cls.query.filter(cls.line_id == lineId).first()

    @classmethod
    def insertKitchen(cls, lineId, orderlineId, tableCode, staffName, cat1, description, description2, unit, quantity,
                      printerName, orderTime, comments, stockType, cat2, salesorderId):
        newKitchen = Kitchen(line_id=lineId,
                             orderline_id=orderlineId,
                             table_code=tableCode,
                             staff_name=staffName,
                             cat1=cat1,
                             description=description,
                             description2=description2,
                             unit=unit,
                             quantity=quantity,
                             printer=printerName,
                             printer2=printerName,
                             order_time=orderTime,
                             handwritting=0,
                             comments=comments,
                             stock_type=stockType,
                             customer_name=tableCode,
                             cat2=cat2,
                             salesorder_id=salesorderId)

        cls.query.session.add(newKitchen)
        cls.query.session.flush()
        # cls.query.session.commit()

        return lineId


class StockPrint(Base):
    __tablename__ = 'StockPrint'
    stock_id = Column(Integer, nullable=False, primary_key=True)
    site_id = Column(Integer, nullable=False)
    printer = Column(Unicode(60), nullable=False)
    printer2 = Column(Unicode(60), nullable=False)
    delivery_docket = Column(BIT)

    @classmethod
    def getPrinter(cls, stockId, siteId):
        return cls.query.filter(cls.stock_id == stockId).filter(or_(cls.site_id == -1, cls.site_id == siteId)).all()


class CatPrint(Base):
    __tablename__ = 'CatPrint'
    Cat_id = Column(Integer, nullable=False, primary_key=True)
    site_id = Column(Integer, nullable=False)
    printer = Column(Unicode(60), nullable=False, primary_key=True)
    printer2 = Column(Unicode(60), nullable=False)
    delivery_docket = Column(BIT)

    @classmethod
    def getPrinter(cls, catId, siteId):
        return cls.query.filter(cls.Cat_id == catId).filter(or_(cls.site_id == -1, cls.site_id == siteId)).all()


class KeyboardPrint(Base):
    __tablename__ = 'KeyboardPrint'
    kb_id = Column(Integer, nullable=False, primary_key=True)
    site_id = Column(Integer, nullable=False)
    printer = Column(Unicode(60), nullable=False)
    printer2 = Column(Unicode(60), nullable=False)
    delivery_docket = Column(BIT)

    @classmethod
    def getPrinter(cls, kbId, siteId):
        return cls.query.filter(cls.kb_id == kbId).filter(or_(cls.site_id == -1, cls.site_id == siteId)).all()


class Customer(Base):
    __tablename__ = 'Customer'
    __table_args__ = (
        Index('Country', 'country', 'customer_id', unique=True),
        Index('Surname', 'surname', 'customer_id', unique=True),
        Index('Customer Name', 'surname', 'given_names', 'customer_id', unique=True),
        Index('Given Names', 'given_names', 'customer_id', unique=True),
        Index('Suburb', 'suburb', 'customer_id', unique=True),
        Index('Custom1', 'custom1', 'customer_id', unique=True),
        Index('Salutation', 'salutation', 'customer_id', unique=True),
        Index('Company', 'company', 'customer_id', unique=True),
        Index('Position', 'position', 'customer_id', unique=True),
        Index('Custom2', 'custom2', 'customer_id', unique=True),
        Index('State', 'state', 'customer_id', unique=True),
        Index('Barcode', 'barcode', 'customer_id', unique=True),
        Index('AC Owner', 'owner_id', 'customer_id', unique=True)
    )

    customer_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    barcode = Column(Unicode(15), nullable=False, unique=True)
    grade = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    notes = Column(Unicode(255), nullable=False)
    comments = Column(Unicode(255), nullable=False)
    status = Column(BIT, nullable=False, server_default=text("(0)"))
    custom1 = Column(Unicode(50), nullable=False)
    custom2 = Column(Unicode(50), nullable=False)
    inactive = Column(BIT, nullable=False, server_default=text("(0)"))
    date_modified = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    surname = Column(Unicode(50), nullable=False)
    given_names = Column(Unicode(50), nullable=False)
    position = Column(Unicode(50), nullable=False)
    company = Column(Unicode(50), nullable=False)
    salutation = Column(Unicode(5), nullable=False)
    account = Column(BIT, nullable=False, server_default=text("(0)"))
    opened_id = Column(ForeignKey('Staff.staff_id'), nullable=False, index=True, server_default=text("(0)"))
    owner_id = Column(ForeignKey('Staff.staff_id'), nullable=False, index=True, server_default=text("(0)"))
    limit = Column(MONEY, nullable=False, server_default=text("(0)"))
    days = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    fromEOM = Column(BIT, nullable=False, server_default=text("(0)"))
    addr1 = Column(Unicode(40), nullable=False)
    addr2 = Column(Unicode(40), nullable=False)
    addr3 = Column(Unicode(40), nullable=False)
    suburb = Column(Unicode(40), nullable=False)
    state = Column(Unicode(30), nullable=False)
    postcode = Column(Unicode(10), nullable=False)
    country = Column(Unicode(20), nullable=False)
    phone = Column(Unicode(20), nullable=False)
    fax = Column(Unicode(20), nullable=False)
    mobile = Column(Unicode(20), nullable=False)
    email = Column(Unicode(50), nullable=False)
    abn = Column(Unicode(11), nullable=False)
    overseas = Column(BIT, nullable=False, server_default=text("(0)"))
    total_points = Column(Integer)
    unclaimed_points = Column(Integer)
    dob = Column(DateTime)
    sex = Column(Unicode(1))
    receive_info = Column(BIT)
    prepaid_amt = Column(MONEY)

    opened = relationship('Staff', primaryjoin='Customer.opened_id == Staff.staff_id')
    owner = relationship('Staff', primaryjoin='Customer.owner_id == Staff.staff_id')


class Payment(Base):
    __tablename__ = 'Payments'

    payment_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    docket_id = Column(ForeignKey('Docket.docket_id'), nullable=False, index=True, server_default=text("(0)"))
    docket_date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    paymenttype = Column(Unicode(15), nullable=False, index=True)
    amount = Column(MONEY, nullable=False, server_default=text("(0)"))
    drawer = Column(Unicode(1), nullable=False, index=True)
    eft_method = Column(SmallInteger, nullable=False, server_default=text("(0)"))

    docket = relationship('Docket')

    @classmethod
    def getAll(cls, date):
        query = cls.query.order_by(cls.payment_id.asc())
        if date:
            # query = query.filter(and_(cls.docket_date >= date, cls.docket_date <= '2012-10-26'))
            query = query.filter(cls.docket_date.between(date + ' 00:00:00', date + ' 23:59:59'))

        res = query.all()
        return res

    @classmethod
    def insertPayment(cls, docketId, docketDate, paymentType, amount):
        max = cls.query.session.query(func.max(cls.payment_id).label("max_id")).one()
        payment_id = 1 if max.max_id is None else max.max_id + 1

        newPayment = Payment(payment_id=payment_id,
                             docket_id=docketId,
                             docket_date=docketDate,
                             paymenttype=paymentType,
                             amount=amount,
                             drawer='O')

        cls.query.session.add(newPayment)
        cls.query.session.flush()
        # cls.query.session.commit()

        return payment_id


class Docket(Base):
    __tablename__ = 'Docket'

    docket_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    docket_date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    staff_id = Column(ForeignKey('Staff.staff_id'), nullable=False, index=True, server_default=text("(0)"))
    customer_id = Column(ForeignKey('Customer.customer_id'), nullable=False, index=True, server_default=text("(0)"))
    transaction = Column(Unicode(2), nullable=False, index=True)
    custom = Column(Unicode(40))
    payment_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    original_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    origin = Column(Integer, nullable=False, server_default=text("(0)"))
    drawer = Column(Unicode(1), nullable=False, index=True)
    comments = Column(Unicode(255), nullable=False)
    subtotal = Column(MONEY, nullable=False, server_default=text("(0)"))
    discount = Column(MONEY, nullable=False, server_default=text("(0)"))
    rounding = Column(MONEY, nullable=False, server_default=text("(0)"))
    total_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    total_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    gp = Column(MONEY, nullable=False, server_default=text("(0)"))
    commission = Column(MONEY, nullable=False, server_default=text("(0)"))
    bonus = Column(MONEY, nullable=False, server_default=text("(0)"))
    archive = Column(BIT, nullable=False, server_default=text("(0)"))
    actual_id = Column(Integer)
    guest_no = Column(SmallInteger)
    points_earned = Column(Integer)
    member_barcode = Column(Unicode(15))

    customer = relationship('Customer')
    staff = relationship('Staff')

    @classmethod
    def getAll(cls, date):
        """获得今天的所有订单"""
        query = cls.query.order_by(cls.docket_date.asc())
        if date:
            # query = query.filter(and_(cls.docket_date >= date, cls.docket_date <= '2012-10-26'))
            query = query.filter(cls.docket_date.between(date + ' 00:00:00', date + ' 23:59:59'))

        res = query.all()
        return res

    @classmethod
    def getByDate(cls, date):
        """获得日期大于给出日子的所有订单"""
        query = cls.query.order_by(cls.docket_date.desc())
        if date:
            query = query.filter(cls.docket_date >= date)

        res = query.all()
        return res

    @classmethod
    def getByDocketId(cls, docketId):
        res = cls.query.filter(cls.docket_id == docketId).first()
        return res

    @classmethod
    def insertDocket(cls, time, staffId, tableCode, amount, guestNo, memberBarcode=None):

        max = cls.query.session.query(func.max(cls.docket_id).label("max_id")).one()
        docket_id = 1 if max.max_id is None else max.max_id + 1

        newDocket = Docket(docket_id=docket_id,
                           docket_date=time,
                           staff_id=staffId,
                           transaction="SA",
                           custom=tableCode,
                           drawer='O',
                           comments='',
                           subtotal=amount,
                           total_ex=amount / 1.1,
                           total_inc=amount,
                           gp=amount / 1.1,
                           actual_id=docket_id,
                           guest_no=guestNo,
                           member_barcode=memberBarcode)

        cls.query.session.add(newDocket)
        cls.query.session.flush()
        # cls.query.session.commit()

        return docket_id


class DocketOnline(Base):
    __tablename__ = 'DocketOnline'

    uuid = Column(Unicode(40), primary_key=True)
    docket_id = Column(Integer, server_default=text("(0)"))
    actual_id = Column(Unicode(40))
    remark = Column(Unicode(40))

    @classmethod
    def getByDocketId(cls, docketId):
        return cls.query.filter(cls.docket_id == docketId).first()

    @classmethod
    def insert(cls, docketId, actualId, remark):
        newSalesorderOnline = DocketOnline(uuid=uuid.uuid1().hex,
                                           docket_id=docketId,
                                           actual_id=actualId,
                                           remark=remark)
        cls.query.session.add(newSalesorderOnline)
        cls.query.session.flush()

        return docketId


class DocketLine(Base):
    __tablename__ = 'DocketLine'

    line_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    docket_id = Column(ForeignKey('Docket.docket_id'), nullable=False, index=True, server_default=text("(0)"))
    stock_id = Column(ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)"))
    cost_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    cost_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    sales_tax = Column(Unicode(3), nullable=False)
    sell_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    sell_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    rrp = Column(MONEY, nullable=False, server_default=text("(0)"))
    print_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    print_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    quantity = Column(Float(53), nullable=False, server_default=text("(0)"))
    customer_id = Column(ForeignKey('Customer.customer_id'), nullable=False, index=True, server_default=text("(0)"))
    serial_no = Column(Unicode(40), nullable=False)
    package_id = Column(Float(53), nullable=False, index=True, server_default=text("(0)"))
    gp = Column(MONEY, nullable=False, server_default=text("(0)"))
    size_level = Column(SmallInteger)

    customer = relationship('Customer')
    docket = relationship('Docket')
    stock = relationship('Stock')

    @classmethod
    def getByDocketId(cls, docketId):
        query = cls.query.order_by(cls.docket_id.asc())
        query = query.filter(cls.docket_id.in_(docketId))
        res = query.all()

        return res

    @classmethod
    def insertDocketLine(cls, docketId, stockId, sizeLevel, price, quantity):
        max = cls.query.session.query(func.max(cls.line_id).label("max_id")).one()
        lineId = 1 if max.max_id is None else max.max_id + 1

        newDocketLine = DocketLine(line_id=lineId,
                                   docket_id=docketId,
                                   stock_id=stockId,
                                   sales_tax='GST',
                                   sell_ex=price / 1.1,
                                   sell_inc=price,
                                   rrp=price,
                                   print_ex=price / 1.1,
                                   print_inc=price,
                                   quantity=quantity,
                                   serial_no=0,
                                   gp=price / 1.1,
                                   size_level=sizeLevel)

        cls.query.session.add(newDocketLine)
        cls.query.session.flush()
        # cls.query.session.commit()

        return lineId


class GlobalSetting(Base):
    __tablename__ = 'GlobalSetting'

    setting_key = Column(Unicode(50), primary_key=True)
    setting_value = Column(Unicode(3000))
    disable = Column(BIT)
    exclude_terminals = Column(Unicode(100))
    file_content = Column(LargeBinary)

    @classmethod
    def getMenuSizeLevelOptionDisallow(cls):
        res = cls.query.filter(cls.disable == 0, cls.setting_key.like('MenuSizeLevelOptionDisallow%')).all()
        return res

    @classmethod
    def getMenuOptionLimitation(cls):
        res = cls.query.filter(cls.disable == 0, cls.setting_key.like('MenuOptionLimitation%')).all()
        return res

    @classmethod
    def deleteAllRules(cls):
        cls.query.filter(or_(cls.setting_key.like('MenuOptionLimitation%'),
                             cls.setting_key.like('MenuSizeLevelOptionDisallow%'))).delete(synchronize_session=False)
        cls.query.session.commit()

    @classmethod
    def insertRules(cls, settingKey, settingValue, disable):
        newRule = GlobalSetting(setting_key=settingKey,
                                setting_value=settingValue,
                                disable=disable)

        cls.query.session.add(newRule)
        cls.query.session.flush()
        cls.query.session.commit()


class GlobalSettingSub(Base):
    __tablename__ = 'GlobalSettingSub'

    setting_key = Column(ForeignKey('GlobalSetting.setting_key'), primary_key=True, nullable=False)
    setting_subkey = Column(Unicode(50), primary_key=True, nullable=False)
    setting_value = Column(Unicode(3000))

    GlobalSetting = relationship('GlobalSetting')
