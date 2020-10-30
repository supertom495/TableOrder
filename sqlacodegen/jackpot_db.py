# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, ForeignKeyConstraint, Index, Integer, LargeBinary, NCHAR, SmallInteger, String, Table, Unicode, UnicodeText, text
from sqlalchemy.dialects.mssql import BIT, MONEY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AccountGrouping(Base):
    __tablename__ = 'Account_Groupings'

    name = Column(Unicode(20), nullable=False, index=True)
    paymenttype = Column(Unicode(15), primary_key=True)
    account = Column(Unicode(20), nullable=False)


class AccountNumber(Base):
    __tablename__ = 'Account_Numbers'

    name = Column(Unicode(20), primary_key=True)
    acn = Column(Unicode(31), nullable=False)
    date_modified = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))


t_Attendance = Table(
    'Attendance', metadata,
    Column('staff_id', Integer, nullable=False),
    Column('drawer', Unicode(1), nullable=False),
    Column('checkin_time', DateTime, nullable=False),
    Column('checkout_time', DateTime, nullable=False),
    Column('comments', Unicode(120)),
    Column('attend_id', Integer)
)


t_AutoIdDocket = Table(
    'AutoIdDocket', metadata,
    Column('id', Integer, nullable=False),
    Column('id2', Integer)
)


t_AutoIdDocketLine = Table(
    'AutoIdDocketLine', metadata,
    Column('id', Integer, nullable=False),
    Column('id2', Integer)
)


t_AutoIdPayments = Table(
    'AutoIdPayments', metadata,
    Column('id', Integer, nullable=False),
    Column('id2', Integer)
)


t_AutoIdSalesOrder = Table(
    'AutoIdSalesOrder', metadata,
    Column('id', Integer, nullable=False),
    Column('id2', Integer)
)


t_AutoIdSalesOrderLine = Table(
    'AutoIdSalesOrderLine', metadata,
    Column('id', Integer, nullable=False),
    Column('id2', Integer)
)


t_Booking = Table(
    'Booking', metadata,
    Column('book_id', Integer, nullable=False),
    Column('book_date', DateTime),
    Column('date_from', DateTime),
    Column('date_to', DateTime),
    Column('time_id', Integer),
    Column('table_id', Integer),
    Column('customer_id', Integer),
    Column('customer_name', Unicode(50)),
    Column('phone', Unicode(50)),
    Column('email', Unicode(60)),
    Column('guest_no', SmallInteger),
    Column('notes', Unicode(255)),
    Column('staff_id', Integer),
    Column('salesorder_id', Integer),
    Column('booking_time', Unicode(40)),
    Column('booking_status', SmallInteger)
)


t_BreakDown = Table(
    'BreakDown', metadata,
    Column('breakdown_id', Integer, nullable=False),
    Column('breakdown_date', DateTime, nullable=False),
    Column('staff_id', Integer, nullable=False),
    Column('stock_id', Integer, nullable=False),
    Column('cost', MONEY, nullable=False),
    Column('sell', MONEY, nullable=False),
    Column('quantity', Float(24), nullable=False),
    Column('comments', Unicode(120))
)


t_BreakDownLine = Table(
    'BreakDownLine', metadata,
    Column('line_id', Integer, nullable=False),
    Column('breakdown_id', Integer, nullable=False),
    Column('stock_id', Integer, nullable=False),
    Column('cost', MONEY, nullable=False),
    Column('sell', MONEY, nullable=False),
    Column('quantity', Float(24), nullable=False)
)


t_ButtonPic = Table(
    'ButtonPic', metadata,
    Column('pic_id', Integer),
    Column('barcode', Unicode(15), index=True),
    Column('date_modified', DateTime),
    Column('pic', LargeBinary)
)


t_CashInOut = Table(
    'CashInOut', metadata,
    Column('seq_id', Integer),
    Column('description', Unicode(128))
)


t_CashInOut_Count = Table(
    'CashInOut_Count', metadata,
    Column('count_id', Integer),
    Column('docket_id', Integer),
    Column('note_type', Unicode(20)),
    Column('note_name', Unicode(20)),
    Column('note_value', MONEY),
    Column('note_count', SmallInteger)
)


t_CashRate = Table(
    'CashRate', metadata,
    Column('cash_name', Unicode(50)),
    Column('rate', Float(53))
)


t_Cashup = Table(
    'Cashup', metadata,
    Column('session_id', Integer, nullable=False),
    Column('staff_id', Integer, nullable=False),
    Column('session_date', DateTime, nullable=False),
    Column('docket_id', Integer, nullable=False),
    Column('drawer', Unicode(1), nullable=False),
    Column('status', SmallInteger, nullable=False),
    Column('comments', Unicode(255), nullable=False),
    Column('stock_value', MONEY, nullable=False),
    Column('stock_variance', MONEY, nullable=False),
    Column('exportation_state', SmallInteger, nullable=False)
)


t_Cashup_Count = Table(
    'Cashup_Count', metadata,
    Column('count_id', Integer),
    Column('session_id', Integer),
    Column('note_type', Unicode(20)),
    Column('note_name', Unicode(20)),
    Column('note_value', MONEY),
    Column('note_count', SmallInteger)
)


t_CatPrint = Table(
    'CatPrint', metadata,
    Column('Cat_id', Integer, nullable=False),
    Column('site_id', Integer, nullable=False),
    Column('printer', Unicode(60), nullable=False),
    Column('printer2', Unicode(60), nullable=False),
    Column('delivery_docket', BIT)
)


t_Category = Table(
    'Category', metadata,
    Column('cat_id', Integer, nullable=False),
    Column('cat_code', Unicode(15), nullable=False),
    Column('cat_name', Unicode(40)),
    Column('cat_name2', Unicode(40), nullable=False),
    Column('time_id', Integer, nullable=False),
    Column('printer', Unicode(80)),
    Column('printer2', Unicode(80)),
    Column('inactive', BIT, nullable=False),
    Column('modifier1', Unicode(20)),
    Column('modifier2', Unicode(20)),
    Column('modifier3', Unicode(20)),
    Column('modifier4', Unicode(20)),
    Column('cat_name3', Unicode(40)),
    Column('cat_name4', Unicode(40))
)


t_ChangeTable = Table(
    'ChangeTable', metadata,
    Column('change_id', Integer, nullable=False),
    Column('table_old', Unicode(20), nullable=False),
    Column('table_new', Unicode(40), nullable=False),
    Column('printer', Unicode(100)),
    Column('printer2', Unicode(100)),
    Column('change_time', DateTime, nullable=False),
    Column('staff_id', Integer)
)


class ChangeTableLine(Base):
    __tablename__ = 'ChangeTableLine'

    change_id = Column(Integer, nullable=False, index=True)
    line_id = Column(Integer, primary_key=True)
    stock_id = Column(Float(53), nullable=False, index=True)
    cost_ex = Column(MONEY, nullable=False)
    cost_inc = Column(MONEY, nullable=False)
    sales_tax = Column(Unicode(3), nullable=False)
    sell_ex = Column(MONEY, nullable=False)
    sell_inc = Column(MONEY, nullable=False)
    rrp = Column(MONEY, nullable=False)
    print_ex = Column(MONEY, nullable=False)
    print_inc = Column(MONEY, nullable=False)
    quantity = Column(Float(53), nullable=False)
    parentline_id = Column(Integer, nullable=False, index=True)
    package = Column(BIT, nullable=False)
    status = Column(SmallInteger, nullable=False)
    orderline_id = Column(Integer, nullable=False, index=True)
    size_level = Column(SmallInteger)
    staff_id = Column(Integer)
    time_ordered = Column(DateTime)
    out_order = Column(SmallInteger)
    hand_writting = Column(BIT)
    seq_id = Column(Integer)
    original_line_id = Column(Integer)


t_ContactLog = Table(
    'ContactLog', metadata,
    Column('log_id', Integer, nullable=False),
    Column('customer_id', Integer, nullable=False),
    Column('contact', String(40, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('log_date', DateTime, nullable=False, index=True),
    Column('elapsed_time', Integer, nullable=False),
    Column('recontact_date', DateTime, nullable=False),
    Column('notes', String(256, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('inactive', BIT)
)


t_Conversion_Errors = Table(
    'Conversion Errors', metadata,
    Column('Object Type', Unicode(255)),
    Column('Object Name', Unicode(255)),
    Column('Error Description', UnicodeText(1073741823))
)


t_Costing = Table(
    'Costing', metadata,
    Column('stock_id', Integer, nullable=False),
    Column('size_rate1', Float(24), nullable=False),
    Column('cost11', MONEY, nullable=False),
    Column('cost12', MONEY, nullable=False),
    Column('cost13', MONEY, nullable=False),
    Column('cost14', MONEY, nullable=False),
    Column('size_rate2', Float(24), nullable=False),
    Column('cost21', MONEY, nullable=False),
    Column('cost22', MONEY, nullable=False),
    Column('cost23', MONEY, nullable=False),
    Column('cost24', MONEY, nullable=False),
    Column('size_rate3', Float(24), nullable=False),
    Column('cost31', MONEY, nullable=False),
    Column('cost32', MONEY, nullable=False),
    Column('cost33', MONEY, nullable=False),
    Column('cost34', MONEY, nullable=False),
    Column('size_rate4', Float(24), nullable=False),
    Column('cost41', MONEY, nullable=False),
    Column('cost42', MONEY, nullable=False),
    Column('cost43', MONEY, nullable=False),
    Column('cost44', MONEY, nullable=False)
)


t_CustPay = Table(
    'CustPay', metadata,
    Column('customer_id', Integer, nullable=False),
    Column('Date', DateTime, nullable=False),
    Column('Transaction', String(25, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ID', Integer, nullable=False),
    Column('Inv Amt', MONEY, nullable=False),
    Column('Paid Amt', MONEY, nullable=False)
)


t_Custom = Table(
    'Custom', metadata,
    Column('module_name', Unicode(20)),
    Column('field_name', Unicode(10)),
    Column('custom_name', Unicode(64))
)


t_DeleteItem = Table(
    'DeleteItem', metadata,
    Column('line_id', Integer, nullable=False),
    Column('table_code', Unicode(20), nullable=False),
    Column('staff_name', Unicode(40), nullable=False),
    Column('cat1', Unicode(20), nullable=False),
    Column('description', Unicode(60)),
    Column('description2', Unicode(60)),
    Column('unit', Unicode(10), nullable=False),
    Column('quantity', Float(24), nullable=False),
    Column('printer', Unicode(100)),
    Column('printer2', Unicode(100)),
    Column('order_time', DateTime, nullable=False),
    Column('reason', Unicode(128), nullable=False),
    Column('sell_inc', MONEY),
    Column('stock_id', Integer)
)


class DocketLinePoint(Base):
    __tablename__ = 'DocketLinePoints'

    docketline_id = Column(Integer, primary_key=True)
    points = Column(Integer, nullable=False)


class DocketOnline(Base):
    __tablename__ = 'DocketOnline'

    uuid = Column(Unicode(40), primary_key=True)
    docket_id = Column(Integer, server_default=text("((0))"))
    actual_id = Column(Unicode(40))
    remark = Column(Unicode(40))


t_Eftpos = Table(
    'Eftpos', metadata,
    Column('docket_id', Integer, nullable=False),
    Column('actual_id', Integer, nullable=False),
    Column('drawer', Unicode(1), nullable=False),
    Column('payment_details', String(512, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('rrn', Unicode(20)),
    Column('auth_code', Unicode(20)),
    Column('track2', Unicode(50)),
    Column('pan', Unicode(20)),
    Column('expiry_date', Unicode(10)),
    Column('account_type', Unicode(20)),
    Column('purchase_amt', MONEY),
    Column('cash_amt', MONEY),
    Column('tip_amt', MONEY),
    Column('pan_source', Unicode(10)),
    Column('stan', Unicode(10))
)


t_ExtraCat = Table(
    'ExtraCat', metadata,
    Column('cat_id', Integer, nullable=False),
    Column('extra_id', Integer, nullable=False),
    Column('visible_type', SmallInteger)
)


t_ExtraStock = Table(
    'ExtraStock', metadata,
    Column('stock_id', Integer, nullable=False),
    Column('extra_id', Integer, nullable=False),
    Column('visible_type', SmallInteger)
)


t_FingerPrint = Table(
    'FingerPrint', metadata,
    Column('staff_id', Integer, nullable=False, index=True),
    Column('date_modified', DateTime),
    Column('finger_print', LargeBinary)
)


t_Functions = Table(
    'Functions', metadata,
    Column('function_id', Integer, nullable=False, index=True),
    Column('function_name', String(50, 'Chinese_PRC_CI_AS')),
    Column('caption', String(50, 'Chinese_PRC_CI_AS')),
    Column('param_name1', String(50, 'Chinese_PRC_CI_AS')),
    Column('param_name2', String(50, 'Chinese_PRC_CI_AS')),
    Column('param_name3', String(50, 'Chinese_PRC_CI_AS')),
    Column('param_value1', String(50, 'Chinese_PRC_CI_AS')),
    Column('param_value2', String(50, 'Chinese_PRC_CI_AS')),
    Column('param_value3', String(50, 'Chinese_PRC_CI_AS')),
    Column('inactive', BIT)
)


t_GiftCard = Table(
    'GiftCard', metadata,
    Column('card_id', Integer, nullable=False),
    Column('docket_id', Integer, nullable=False),
    Column('barcode', Unicode(15)),
    Column('issue_date', DateTime),
    Column('expiry_date', DateTime),
    Column('init_amount', MONEY),
    Column('curr_amount', MONEY)
)


class GlobalSetting(Base):
    __tablename__ = 'GlobalSetting'

    setting_key = Column(Unicode(50), primary_key=True)
    setting_value = Column(Unicode(3000))
    disable = Column(BIT)
    exclude_terminals = Column(Unicode(100))
    file_content = Column(LargeBinary)


t_GlobalSysInfo = Table(
    'GlobalSysInfo', metadata,
    Column('syskey', Unicode(20), nullable=False),
    Column('sysval', Unicode(255), nullable=False),
    Column('date_modified', DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
)


class GoodsDocket(Base):
    __tablename__ = 'GoodsDocket'

    docket_id = Column(Integer, primary_key=True)
    docket_date = Column(DateTime, nullable=False)
    staff_id = Column(Integer, nullable=False)
    supplier_id = Column(Integer, nullable=False)
    transaction = Column(Unicode(2), nullable=False)
    custom = Column(Unicode(20))
    payment_id = Column(Integer, nullable=False)
    original_id = Column(Integer, nullable=False)
    origin = Column(Integer, nullable=False)
    comments = Column(Unicode(255))
    subtotal = Column(MONEY, nullable=False)
    discount = Column(MONEY, nullable=False)
    total_ex = Column(MONEY, nullable=False)
    total_inc = Column(MONEY, nullable=False)


t_GoodsList = Table(
    'GoodsList', metadata,
    Column('list_id', Integer),
    Column('list_name', NCHAR(20)),
    Column('supplier_id', Integer),
    Column('date_modified', DateTime)
)


t_GoodsListLine = Table(
    'GoodsListLine', metadata,
    Column('list_type', NCHAR(1)),
    Column('list_id', Integer),
    Column('stock_id', Integer),
    Column('barcode', NCHAR(15)),
    Column('item_code', NCHAR(16)),
    Column('description', NCHAR(128)),
    Column('longdesc', NCHAR(200)),
    Column('goods_tax', NCHAR(3)),
    Column('cost', MONEY),
    Column('sell', MONEY),
    Column('quantity', Float(24)),
    Column('Packing', Float(24))
)


t_GoodsPay = Table(
    'GoodsPay', metadata,
    Column('supplier_id', Integer, nullable=False),
    Column('Date', DateTime, nullable=False),
    Column('Transaction', Unicode(24), nullable=False),
    Column('due_date', DateTime),
    Column('ID', Integer, nullable=False),
    Column('Inv Amt', MONEY, nullable=False),
    Column('Paid Amt', MONEY, nullable=False),
    Column('GRTotal', MONEY, nullable=False)
)


t_GroupRights = Table(
    'GroupRights', metadata,
    Column('group_id', Integer),
    Column('right_id', Integer),
    Column('disabled', Integer)
)


t_Keyboard = Table(
    'Keyboard', metadata,
    Column('kb_id', Integer, nullable=False),
    Column('kb_name', Unicode(64), nullable=False),
    Column('btn_page', Integer, nullable=False),
    Column('btn_left', Integer, nullable=False),
    Column('btn_top', Integer, nullable=False),
    Column('btn_width', Integer, nullable=False),
    Column('btn_height', Integer, nullable=False),
    Column('btn_forecolor', Integer, nullable=False),
    Column('btn_backcolor', Integer, nullable=False),
    Column('btn_fontname', Unicode(64), nullable=False),
    Column('btn_fontsize', Integer, nullable=False),
    Column('btn_showpic', BIT, nullable=False),
    Column('cat_cols', SmallInteger),
    Column('cat_height', SmallInteger),
    Column('kb_name2', Unicode(20)),
    Column('cat_rows', SmallInteger),
    Column('menu_type_id', Integer),
    Column('menu_type_limit', Integer)
)


t_KeyboardCat = Table(
    'KeyboardCat', metadata,
    Column('cat_id', Integer, nullable=False),
    Column('cat_name', Unicode(64), nullable=False),
    Column('kb_id', Integer, nullable=False),
    Column('btn_page', Integer, nullable=False),
    Column('btn_left', Integer, nullable=False),
    Column('btn_top', Integer, nullable=False),
    Column('btn_width', Integer, nullable=False),
    Column('btn_height', Integer, nullable=False),
    Column('btn_forecolor', Integer, nullable=False),
    Column('btn_backcolor', Integer, nullable=False),
    Column('btn_fontname', Unicode(64), nullable=False),
    Column('btn_fontsize', Integer, nullable=False),
    Column('btn_showpic', BIT, nullable=False),
    Column('btn_rows', SmallInteger),
    Column('btn_cols', SmallInteger),
    Column('pic_align', SmallInteger),
    Column('text_align', SmallInteger),
    Column('invisible', BIT)
)


t_KeyboardCatPDA = Table(
    'KeyboardCatPDA', metadata,
    Column('cat_id', Integer, nullable=False),
    Column('cat_name', Unicode(64), nullable=False),
    Column('kb_id', Integer, nullable=False),
    Column('btn_page', Integer, nullable=False),
    Column('btn_left', Integer, nullable=False),
    Column('btn_top', Integer, nullable=False),
    Column('btn_width', Integer, nullable=False),
    Column('btn_height', Integer, nullable=False),
    Column('btn_forecolor', Integer, nullable=False),
    Column('btn_backcolor', Integer, nullable=False),
    Column('btn_fontname', Unicode(64), nullable=False),
    Column('btn_fontsize', Integer, nullable=False),
    Column('btn_showpic', BIT, nullable=False),
    Column('btn_rows', SmallInteger),
    Column('btn_cols', SmallInteger),
    Column('pic_align', SmallInteger),
    Column('text_align', SmallInteger),
    Column('invisible', BIT)
)


t_KeyboardItem = Table(
    'KeyboardItem', metadata,
    Column('item_id', Integer, nullable=False),
    Column('item_barcode', Unicode(24), nullable=False),
    Column('item_name', Unicode(64), nullable=False),
    Column('cat_id', Integer, nullable=False),
    Column('kb_id', Integer, nullable=False),
    Column('btn_page', Integer, nullable=False),
    Column('btn_left', Integer, nullable=False),
    Column('btn_top', Integer, nullable=False),
    Column('btn_width', Integer, nullable=False),
    Column('btn_height', Integer, nullable=False),
    Column('btn_forecolor', Integer, nullable=False),
    Column('btn_backcolor', Integer, nullable=False),
    Column('btn_fontname', Unicode(64), nullable=False),
    Column('btn_fontsize', Integer, nullable=False),
    Column('btn_showpic', BIT, nullable=False),
    Column('btn_showprice', BIT),
    Column('subcat_id', Integer),
    Column('stock_id', Integer),
    Column('subcat_link', Unicode(999))
)


t_KeyboardItemPDA = Table(
    'KeyboardItemPDA', metadata,
    Column('item_id', Integer, nullable=False),
    Column('item_barcode', Unicode(24), nullable=False),
    Column('item_name', Unicode(64), nullable=False),
    Column('cat_id', Integer, nullable=False),
    Column('kb_id', Integer, nullable=False),
    Column('btn_page', Integer, nullable=False),
    Column('btn_left', Integer, nullable=False),
    Column('btn_top', Integer, nullable=False),
    Column('btn_width', Integer, nullable=False),
    Column('btn_height', Integer, nullable=False),
    Column('btn_forecolor', Integer, nullable=False),
    Column('btn_backcolor', Integer, nullable=False),
    Column('btn_fontname', Unicode(64), nullable=False),
    Column('btn_fontsize', Integer, nullable=False),
    Column('btn_showpic', BIT, nullable=False),
    Column('btn_showprice', BIT, nullable=False),
    Column('subcat_id', Integer)
)


t_KeyboardPDA = Table(
    'KeyboardPDA', metadata,
    Column('kb_id', Integer, nullable=False),
    Column('kb_name', Unicode(64), nullable=False),
    Column('btn_page', Integer, nullable=False),
    Column('btn_left', Integer, nullable=False),
    Column('btn_top', Integer, nullable=False),
    Column('btn_width', Integer, nullable=False),
    Column('btn_height', Integer, nullable=False),
    Column('btn_forecolor', Integer, nullable=False),
    Column('btn_backcolor', Integer, nullable=False),
    Column('btn_fontname', Unicode(64), nullable=False),
    Column('btn_fontsize', Integer, nullable=False),
    Column('btn_showpic', BIT, nullable=False),
    Column('cat_cols', SmallInteger),
    Column('cat_height', SmallInteger),
    Column('kb_name2', Unicode(20))
)


t_KeyboardPrint = Table(
    'KeyboardPrint', metadata,
    Column('kb_id', Integer, nullable=False),
    Column('site_id', Integer, nullable=False),
    Column('printer', Unicode(60), nullable=False),
    Column('printer2', Unicode(60), nullable=False),
    Column('delivery_docket', BIT)
)


t_Kitchen = Table(
    'Kitchen', metadata,
    Column('line_id', Integer, nullable=False),
    Column('orderline_id', Integer, nullable=False),
    Column('table_code', Unicode(40)),
    Column('staff_name', Unicode(40), nullable=False),
    Column('cat1', Unicode(40)),
    Column('description', Unicode(60)),
    Column('description2', Unicode(60)),
    Column('unit', Unicode(30)),
    Column('quantity', Float(24), nullable=False),
    Column('printer', Unicode(100)),
    Column('printer2', Unicode(100)),
    Column('order_time', DateTime, nullable=False),
    Column('handwritting', BIT, nullable=False),
    Column('comments', Unicode(200)),
    Column('stock_type', SmallInteger),
    Column('out_order', SmallInteger),
    Column('customer_name', Unicode(40)),
    Column('cat2', Unicode(40)),
    Column('salesorder_id', Integer),
    Column('status', SmallInteger),
    Column('original_line_id', Integer)
)


t_KitchenBackup = Table(
    'KitchenBackup', metadata,
    Column('line_id', Integer, nullable=False),
    Column('orderline_id', Integer, nullable=False),
    Column('table_code', Unicode(40)),
    Column('staff_name', Unicode(40), nullable=False),
    Column('cat1', Unicode(20), nullable=False),
    Column('description', Unicode(60)),
    Column('description2', Unicode(60)),
    Column('unit', Unicode(30)),
    Column('quantity', Float(24), nullable=False),
    Column('printer', Unicode(100)),
    Column('printer2', Unicode(100)),
    Column('order_time', DateTime, nullable=False),
    Column('handwritting', BIT, nullable=False),
    Column('comments', Unicode(200)),
    Column('stock_type', SmallInteger),
    Column('out_order', SmallInteger),
    Column('customer_name', Unicode(40)),
    Column('cat2', Unicode(20)),
    Column('salesorder_id', Integer)
)


t_KitchenReady = Table(
    'KitchenReady', metadata,
    Column('table_code', Unicode(15), nullable=False),
    Column('time_ready', DateTime, nullable=False)
)


t_LedLog = Table(
    'LedLog', metadata,
    Column('log_id', Integer),
    Column('led_num', Unicode(5)),
    Column('stock_id', Integer),
    Column('staff_id', Integer),
    Column('start_time', DateTime),
    Column('end_time', DateTime)
)


t_LedNum = Table(
    'LedNum', metadata,
    Column('led_id', Integer),
    Column('led_time', DateTime),
    Column('led_type', SmallInteger),
    Column('led_num', Unicode(5))
)


t_LedNumBak = Table(
    'LedNumBak', metadata,
    Column('led_id', Integer),
    Column('led_time', DateTime),
    Column('led_type', SmallInteger),
    Column('led_num', Unicode(5)),
    Column('bak_time', DateTime)
)


t_NoSale = Table(
    'NoSale', metadata,
    Column('nosale_id', Integer, nullable=False),
    Column('nosale_date', DateTime),
    Column('drawer', Unicode(1)),
    Column('staff_id', Integer)
)


t_POSCtrl = Table(
    'POSCtrl', metadata,
    Column('cmd_id', Integer, nullable=False),
    Column('cmd_date', DateTime, nullable=False),
    Column('cmd_to', Unicode(40), nullable=False),
    Column('cmd_name', Unicode(100), nullable=False),
    Column('status', SmallInteger)
)


t_POSCtrlLog = Table(
    'POSCtrlLog', metadata,
    Column('log_id', Integer, nullable=False),
    Column('cmd_id', Integer, nullable=False),
    Column('log_date', DateTime, nullable=False),
    Column('log_by', Unicode(40), nullable=False),
    Column('func_name', Unicode(40), nullable=False),
    Column('log_text', Unicode(250), nullable=False),
    Column('status', SmallInteger)
)


t_POSEventSetting = Table(
    'POSEventSetting', metadata,
    Column('event_id', Integer, nullable=False),
    Column('type_id', Integer, nullable=False),
    Column('message', Unicode(150), nullable=False),
    Column('param1', Unicode(20)),
    Column('param2', Unicode(20)),
    Column('param3', Unicode(20))
)


t_POSEventType = Table(
    'POSEventType', metadata,
    Column('type_id', Integer, nullable=False),
    Column('event_type', Unicode(20), nullable=False),
    Column('description', Unicode(50), nullable=False),
    Column('message', Unicode(150), nullable=False),
    Column('params', SmallInteger, nullable=False),
    Column('param_name1', Unicode(20)),
    Column('param_name2', Unicode(20)),
    Column('param_name3', Unicode(20)),
    Column('param1', Unicode(20)),
    Column('param2', Unicode(20)),
    Column('param3', Unicode(20))
)


t_PackageGroup = Table(
    'PackageGroup', metadata,
    Column('group_name', Unicode(15), nullable=False, index=True),
    Column('package_id', Float(53), nullable=False, index=True),
    Column('stock_id', Float(53), nullable=False, index=True),
    Column('sell_inc', MONEY, nullable=False),
    Column('quantity', Float(53), nullable=False),
    Column('date_modified', DateTime, nullable=False),
    Column('sell_inc2', MONEY),
    Column('sell_inc3', MONEY),
    Column('sell_inc4', MONEY)
)


t_Pagers = Table(
    'Pagers', metadata,
    Column('pager_id', Integer, nullable=False),
    Column('salesorder_id', Integer, nullable=False),
    Column('status', SmallInteger, nullable=False)
)


t_Passbook = Table(
    'Passbook', metadata,
    Column('passbook_id', Unicode(50), nullable=False),
    Column('barcode', Unicode(15), nullable=False),
    Column('url', Unicode(300))
)


t_PassbookUpdate = Table(
    'PassbookUpdate', metadata,
    Column('update_id', Integer, nullable=False),
    Column('docket_id', Integer, nullable=False),
    Column('barcode', Unicode(15), nullable=False),
    Column('passbook_id', Unicode(50), nullable=False),
    Column('update_type', Unicode(20)),
    Column('update_value', Unicode(100)),
    Column('update_value2', Unicode(100)),
    Column('update_value3', Unicode(100)),
    Column('date_updated', DateTime),
    Column('status', SmallInteger),
    Column('result', BIT)
)


t_PaymentType = Table(
    'PaymentType', metadata,
    Column('paymenttype', Unicode(50)),
    Column('surcharge', Float(24))
)


class PaymentsForeign(Base):
    __tablename__ = 'PaymentsForeign'

    payment_id = Column(Integer, primary_key=True)
    docket_date = Column(DateTime, nullable=False)
    docket_id = Column(Integer, nullable=False)
    foreign_dollar = Column(Unicode(5))
    rate = Column(Float(53), nullable=False)
    amount = Column(MONEY, nullable=False)
    drawer = Column(Unicode(1))


class PaymentsGood(Base):
    __tablename__ = 'PaymentsGoods'

    payment_id = Column(Integer, primary_key=True)
    docket_id = Column(Integer, nullable=False)
    docket_date = Column(DateTime, nullable=False)
    paymenttype = Column(Unicode(15), nullable=False)
    amount = Column(MONEY, nullable=False)
    payment_ref = Column(Unicode(50))


t_PaymentsWeChat = Table(
    'PaymentsWeChat', metadata,
    Column('pay_number', Unicode(200), nullable=False, index=True),
    Column('paid_amount', MONEY),
    Column('paid_time', DateTime),
    Column('original_number', Unicode(200), index=True),
    Column('transaction_id', Unicode(200)),
    Column('staff_id', Integer),
    Column('docket_id', Integer),
    Column('actual_id', Integer),
    Column('terminal_number', Unicode(50)),
    Column('drawer', Unicode(20)),
    Column('custom1', Unicode(200)),
    Column('custom2', Unicode(200)),
    Column('comments', Unicode(200)),
    Column('payment_details', Unicode(1024)),
    Index('PaymentsWeChat_Idx5', 'paid_time', 'transaction_id'),
    Index('PaymentsWeChatIdx6', 'paid_time', 'original_number'),
    Index('PaymentsWeChat_Idx3', 'docket_id', 'staff_id', 'drawer')
)


class PosEvent(Base):
    __tablename__ = 'PosEvent'

    pos_event_id = Column(Integer, primary_key=True)
    occur_time = Column(DateTime, index=True)
    staff_name = Column(Unicode(50))
    event_source = Column(Unicode(50))
    event_description = Column(Unicode(200))
    event_content = Column(Unicode(500), nullable=False)
    event_type = Column(Unicode(10))
    sent_time = Column(DateTime, index=True)


t_PosLog = Table(
    'PosLog', metadata,
    Column('occur_time', DateTime, nullable=False, index=True),
    Column('log_type', SmallInteger),
    Column('staff_id', Integer),
    Column('computer_name', Unicode(100)),
    Column('log_content', Unicode(300), nullable=False)
)


t_PrepaidCode = Table(
    'PrepaidCode', metadata,
    Column('code_id', Integer, nullable=False, index=True),
    Column('barcode', Unicode(15), nullable=False),
    Column('prepaid_code', Unicode(20), nullable=False),
    Column('amount', MONEY, nullable=False),
    Column('inactive', BIT, nullable=False)
)


t_PriceSchedule = Table(
    'PriceSchedule', metadata,
    Column('schedule_id', Integer),
    Column('stock_id', Integer),
    Column('sell', MONEY),
    Column('effect_time', DateTime),
    Column('inactive', BIT),
    Column('sell2', MONEY),
    Column('sell3', MONEY),
    Column('sell4', MONEY),
    Column('frequency', SmallInteger)
)


class PricingCategory(Base):
    __tablename__ = 'Pricing_Categories'

    Cat = Column(Unicode(20), primary_key=True, nullable=False)
    Sub = Column(Unicode(20), primary_key=True, nullable=False)
    DefaultRule = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    RuleA = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    RuleB = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    RuleC = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    RuleD = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    DefaultValue = Column(Float(53), nullable=False, server_default=text("(0)"))
    ValueA = Column(Float(53), nullable=False, server_default=text("(0)"))
    ValueB = Column(Float(53), nullable=False, server_default=text("(0)"))
    ValueC = Column(Float(53), nullable=False, server_default=text("(0)"))
    ValueD = Column(Float(53), nullable=False, server_default=text("(0)"))
    date_modified = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    date_from = Column(DateTime)
    date_to = Column(DateTime)


t_Pricing_Global = Table(
    'Pricing_Global', metadata,
    Column('DefaultRule', SmallInteger, nullable=False, server_default=text("(0)")),
    Column('RuleA', SmallInteger, nullable=False, server_default=text("(0)")),
    Column('RuleB', SmallInteger, nullable=False, server_default=text("(0)")),
    Column('RuleC', SmallInteger, nullable=False, server_default=text("(0)")),
    Column('RuleD', SmallInteger, nullable=False, server_default=text("(0)")),
    Column('DefaultValue', Float(53), nullable=False, server_default=text("(0)")),
    Column('ValueA', Float(53), nullable=False, server_default=text("(0)")),
    Column('ValueB', Float(53), nullable=False, server_default=text("(0)")),
    Column('ValueC', Float(53), nullable=False, server_default=text("(0)")),
    Column('ValueD', Float(53), nullable=False, server_default=text("(0)")),
    Column('date_modified', DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')")),
    Column('date_from', DateTime),
    Column('date_to', DateTime)
)


t_Printers = Table(
    'Printers', metadata,
    Column('printer', Unicode(80), nullable=False),
    Column('printer2', Unicode(80), nullable=False),
    Column('print_qty', SmallInteger, nullable=False),
    Column('inactive', BIT, nullable=False),
    Column('redirect', BIT, nullable=False),
    Column('printer_redirect', Unicode(80), nullable=False),
    Column('redirect_time', DateTime, nullable=False),
    Column('ip', Unicode(50)),
    Column('port', Integer),
    Column('redirect_on', SmallInteger),
    Column('status', Integer),
    Column('printer_model', Unicode(100)),
    Column('printer_redirect2', Unicode(80))
)


t_REA60 = Table(
    'REA60', metadata,
    Column('REA6A', Unicode(255), nullable=False),
    Column('REA74', Unicode(255), nullable=False),
    Column('REA7E', Unicode(255), nullable=False),
    Column('REA88', Unicode(255), nullable=False),
    Column('REA92', Unicode(255), nullable=False),
    Column('REA9C', Unicode(255), nullable=False),
    Column('REAA6', Unicode(255), nullable=False),
    Column('REAB0', Unicode(255), nullable=False),
    Column('REABA', Unicode(255), nullable=False),
    Column('REAC4', Unicode(255), nullable=False),
    Column('REACE', Unicode(255), nullable=False),
    Column('READ8', Unicode(255), nullable=False),
    Column('REAE2', Unicode(255), nullable=False),
    Column('REAEC', Unicode(255), nullable=False),
    Column('REAF6', Unicode(255), nullable=False),
    Column('REB00', Unicode(255), nullable=False),
    Column('REB0A', Unicode(255), nullable=False),
    Column('REB14', Unicode(255), nullable=False),
    Column('REB1E', Unicode(255), nullable=False),
    Column('REB28', Unicode(255), nullable=False),
    Column('REB32', Unicode(255), nullable=False),
    Column('REB3C', Unicode(255), nullable=False),
    Column('REB46', Unicode(255), nullable=False)
)


t_RME = Table(
    'RME', metadata,
    Column('version', Float(53)),
    Column('working', Integer),
    Column('sale_points', Integer),
    Column('points_value', MONEY),
    Column('freebonus_cat', Unicode(80)),
    Column('freebonus_qty', SmallInteger),
    Column('curr_kb', Integer),
    Column('max_claim_amt', MONEY)
)


t_RandomNum = Table(
    'RandomNum', metadata,
    Column('num_id', SmallInteger, nullable=False),
    Column('random_num', SmallInteger, nullable=False)
)


t_Reasons = Table(
    'Reasons', metadata,
    Column('reason_code', Unicode(10), nullable=False),
    Column('reason', Unicode(60), nullable=False)
)


t_Recipe = Table(
    'Recipe', metadata,
    Column('recipe_id', Integer, nullable=False),
    Column('stock_id', Integer, nullable=False),
    Column('quantity', Float(24), nullable=False),
    Column('cost_ex', MONEY, nullable=False),
    Column('cost_ex2', MONEY, nullable=False),
    Column('cost_ex3', MONEY, nullable=False),
    Column('cost_ex4', MONEY, nullable=False),
    Column('date_modified', DateTime, nullable=False),
    Column('inactive', BIT)
)


class RecordedDate(Base):
    __tablename__ = 'RecordedDate'

    date_type = Column(Integer, primary_key=True)
    date_modified = Column(DateTime, nullable=False)
    remark = Column(Unicode(50))


t_STHist = Table(
    'STHist', metadata,
    Column('st_id', Integer, nullable=False),
    Column('staff_id', Integer, nullable=False),
    Column('st_date', DateTime, nullable=False),
    Column('changed_qty', Float(24), nullable=False),
    Column('total_variance', MONEY, nullable=False),
    Column('comments', Unicode(100))
)


t_STHistLine = Table(
    'STHistLine', metadata,
    Column('st_id', Integer, nullable=False),
    Column('stocktake_date', DateTime, nullable=False),
    Column('stock_id', Float(53), nullable=False),
    Column('quantity', Float(53), nullable=False),
    Column('date_modified', DateTime, nullable=False),
    Column('current_qty', Float(24))
)


t_SaleID = Table(
    'SaleID', metadata,
    Column('sale_type', Integer, nullable=False),
    Column('sale_id', Integer, nullable=False),
    Column('date_modified', DateTime, nullable=False)
)


class SalesOrderBackup(Base):
    __tablename__ = 'SalesOrderBackup'

    salesorder_id = Column(Integer, primary_key=True, nullable=False)
    salesorder_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    staff_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)
    transaction = Column(Unicode(2), nullable=False)
    original_id = Column(Integer, nullable=False)
    custom = Column(Unicode(40))
    comments = Column(Unicode(255), nullable=False)
    subtotal = Column(MONEY, nullable=False)
    discount = Column(MONEY, nullable=False)
    rounding = Column(MONEY, nullable=False)
    total_ex = Column(MONEY, nullable=False)
    total_inc = Column(MONEY, nullable=False)
    status = Column(SmallInteger, nullable=False)
    exported = Column(BIT, nullable=False)
    guest_no = Column(SmallInteger)
    customer_name = Column(Unicode(40))
    backup_time = Column(DateTime, primary_key=True, nullable=False)
    terminal_name = Column(Unicode(50), primary_key=True, nullable=False)
    backup_id = Column(Integer)


class SalesOrderDescSPO(Base):
    __tablename__ = 'SalesOrderDescSPO'

    line_id = Column(Integer, primary_key=True)
    description = Column(Unicode(200))


class SalesOrderLineOnline(Base):
    __tablename__ = 'SalesOrderLineOnline'

    uuid = Column(Unicode(40), primary_key=True)
    line_id = Column(Integer, server_default=text("((0))"))
    salesorder_id = Column(Integer, nullable=False, index=True, server_default=text("((0))"))
    actual_id = Column(Unicode(40))
    actual_line_id = Column(Unicode(40))
    stock_id = Column(Integer, nullable=False, index=True, server_default=text("((0))"))
    quantity = Column(Float(53), nullable=False, server_default=text("((0))"))
    size_level = Column(SmallInteger)
    status = Column(SmallInteger, nullable=False, server_default=text("((0))"))
    type = Column(Unicode(40))


t_SalesOrderLineTmp = Table(
    'SalesOrderLineTmp', metadata,
    Column('line_id', Integer, nullable=False),
    Column('salesorder_id', Integer, nullable=False),
    Column('stock_id', Float(53), nullable=False),
    Column('cost_ex', MONEY, nullable=False),
    Column('cost_inc', MONEY, nullable=False),
    Column('sales_tax', Unicode(3), nullable=False),
    Column('sell_ex', MONEY, nullable=False),
    Column('sell_inc', MONEY, nullable=False),
    Column('rrp', MONEY, nullable=False),
    Column('print_ex', MONEY, nullable=False),
    Column('print_inc', MONEY, nullable=False),
    Column('quantity', Float(53), nullable=False),
    Column('parentline_id', Integer, nullable=False),
    Column('package', BIT, nullable=False),
    Column('status', SmallInteger, nullable=False),
    Column('orderline_id', Integer, nullable=False),
    Column('size_level', SmallInteger),
    Column('staff_id', Integer),
    Column('time_ordered', DateTime),
    Column('out_order', SmallInteger),
    Column('hand_writting', BIT),
    Column('seq_id', Integer),
    Column('original_line_id', Integer)
)


class SalesOrderOnline(Base):
    __tablename__ = 'SalesOrderOnline'

    uuid = Column(Unicode(40), primary_key=True)
    salesorder_id = Column(Integer, server_default=text("((0))"))
    actual_id = Column(Unicode(40))
    remark = Column(Unicode(40))
    status = Column(SmallInteger, nullable=False, server_default=text("((0))"))


class SalesOrderSPO(Base):
    __tablename__ = 'SalesOrderSPO'

    salesorder_id = Column(Integer, primary_key=True)
    salesorder_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    staff_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)
    transaction = Column(Unicode(2), nullable=False)
    original_id = Column(Integer, nullable=False)
    custom = Column(Unicode(40))
    comments = Column(Unicode(255), nullable=False)
    subtotal = Column(MONEY, nullable=False)
    discount = Column(MONEY, nullable=False)
    rounding = Column(MONEY, nullable=False)
    total_ex = Column(MONEY, nullable=False)
    total_inc = Column(MONEY, nullable=False)
    status = Column(SmallInteger, nullable=False)
    exported = Column(BIT, nullable=False)
    guest_no = Column(SmallInteger)
    customer_name = Column(Unicode(40))


t_ScaleBarcode = Table(
    'ScaleBarcode', metadata,
    Column('label_id', Integer, nullable=False),
    Column('trigger_code', Unicode(5), nullable=False),
    Column('total_length', SmallInteger, nullable=False),
    Column('barcode_position', SmallInteger, nullable=False),
    Column('barcode_length', SmallInteger, nullable=False),
    Column('qty_position', SmallInteger, nullable=False),
    Column('qty_length', SmallInteger, nullable=False),
    Column('qty_decimal', SmallInteger, nullable=False),
    Column('price_position', SmallInteger, nullable=False),
    Column('price_length', SmallInteger, nullable=False),
    Column('price_decimal', SmallInteger, nullable=False),
    Column('checksum_position', SmallInteger, nullable=False),
    Column('inactive', BIT, nullable=False)
)


t_ScreenItem = Table(
    'ScreenItem', metadata,
    Column('item_id', Integer, nullable=False, index=True),
    Column('screen_id', Integer, nullable=False),
    Column('layer_id', Integer, nullable=False),
    Column('caption', String(60, 'Chinese_PRC_CI_AS')),
    Column('row', SmallInteger),
    Column('col', SmallInteger),
    Column('height', SmallInteger),
    Column('width', SmallInteger),
    Column('forecolor', Integer),
    Column('backcolor', Integer),
    Column('fontname', Unicode(30)),
    Column('fontsize', Float(24)),
    Column('fontbold', BIT),
    Column('visible', BIT),
    Column('function_id', Integer, nullable=False),
    Column('param_value1', String(50, 'Chinese_PRC_CI_AS')),
    Column('param_value2', String(50, 'Chinese_PRC_CI_AS')),
    Column('param_value3', String(50, 'Chinese_PRC_CI_AS'))
)


t_Screens = Table(
    'Screens', metadata,
    Column('screen_id', Integer, nullable=False, index=True),
    Column('screen_name', Unicode(50)),
    Column('grid_rows', SmallInteger),
    Column('grid_cols', SmallInteger),
    Column('forecolor', Integer),
    Column('backcolor', Integer),
    Column('fontname', Unicode(30)),
    Column('fontsize', Float(24)),
    Column('fontbold', BIT)
)


t_SerialNo = Table(
    'SerialNo', metadata,
    Column('stock_id', Integer),
    Column('serial_no', Unicode(64))
)


t_Site = Table(
    'Site', metadata,
    Column('site_id', Integer, nullable=False),
    Column('site_code', Unicode(15), nullable=False),
    Column('site_name', Unicode(20), nullable=False),
    Column('site_name2', Unicode(20), nullable=False),
    Column('inactive', BIT, nullable=False),
    Column('printer', Unicode(60)),
    Column('printer2', Unicode(60))
)


class SpecialOrder(Base):
    __tablename__ = 'SpecialOrder'

    special_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    order_date = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    staff_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    customer_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    supplier_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    stock_id = Column(Float(53), nullable=False, index=True, server_default=text("(0)"))
    sell_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    sales_tax = Column(Unicode(3), nullable=False)
    quantity = Column(Float(53), nullable=False, server_default=text("(0)"))
    status = Column(SmallInteger, nullable=False, index=True, server_default=text("(0)"))
    line_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))


class SplitPayment(Base):
    __tablename__ = 'SplitPayment'

    uuid = Column(Unicode(40), primary_key=True)
    rrn = Column(Unicode(40))
    salesorder_id = Column(Integer, nullable=False, index=True, server_default=text("((0))"))
    date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    paymenttype = Column(Unicode(15), nullable=False, index=True)
    amount = Column(MONEY, nullable=False, server_default=text("((0))"))
    drawer = Column(Unicode(1), nullable=False, index=True)
    eft_method = Column(SmallInteger, nullable=False, server_default=text("((0))"))


class Staff(Base):
    __tablename__ = 'Staff'
    __table_args__ = (
        Index('Barcode', 'barcode', 'staff_id', unique=True),
        Index('Given Names', 'given_names', 'staff_id', unique=True),
        Index('Docket Name', 'docket_name', 'staff_id', unique=True),
        Index('Custom2', 'custom2', 'staff_id', unique=True),
        Index('Suburb', 'suburb', 'staff_id', unique=True),
        Index('Surname', 'surname', 'staff_id', unique=True),
        Index('Position', 'position', 'staff_id', unique=True),
        Index('Custom1', 'custom1', 'staff_id', unique=True),
        Index('State', 'state', 'staff_id', unique=True)
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


t_StaffGroup = Table(
    'StaffGroup', metadata,
    Column('group_id', Integer),
    Column('group_name', Unicode(40)),
    Column('inactive', BIT)
)


t_StaffLogin = Table(
    'StaffLogin', metadata,
    Column('staff_id', Integer, nullable=False),
    Column('drawer', Unicode(1), nullable=False),
    Column('login_time', DateTime, nullable=False),
    Column('logout_time', DateTime, nullable=False)
)


t_StaffRights = Table(
    'StaffRights', metadata,
    Column('staff_id', Integer),
    Column('right_id', Integer),
    Column('disabled', Integer)
)


t_StockCost = Table(
    'StockCost', metadata,
    Column('stock_id', Integer, nullable=False, index=True),
    Column('freight', Float(24)),
    Column('margin', Float(24)),
    Column('margin2', Float(24)),
    Column('margin3', Float(24)),
    Column('margin4', Float(24)),
    Column('factor1', Float(24)),
    Column('factor2', Float(24)),
    Column('factor3', Float(24)),
    Column('factor4', Float(24))
)


t_StockPic = Table(
    'StockPic', metadata,
    Column('stock_id', Integer, index=True),
    Column('date_modified', DateTime),
    Column('pic', LargeBinary)
)


t_StockPrint = Table(
    'StockPrint', metadata,
    Column('stock_id', Integer, nullable=False),
    Column('site_id', Integer, nullable=False),
    Column('printer', Unicode(60), nullable=False),
    Column('printer2', Unicode(60), nullable=False),
    Column('delivery_docket', BIT)
)


t_SubTables = Table(
    'SubTables', metadata,
    Column('subtable_id', Integer, nullable=False),
    Column('table_id', Integer, nullable=False),
    Column('subtable_code', Unicode(20)),
    Column('table_status', SmallInteger),
    Column('seat', SmallInteger),
    Column('staff_id', Integer),
    Column('logon_time', DateTime),
    Column('computer_user', Unicode(60))
)


t_Suggestion = Table(
    'Suggestion', metadata,
    Column('suggestion_id', Integer, nullable=False, index=True),
    Column('description', Unicode(50), nullable=False),
    Column('date_modified', DateTime, nullable=False),
    Column('date_from', DateTime, nullable=False),
    Column('date_to', DateTime, nullable=False),
    Column('time_from', DateTime, nullable=False),
    Column('time_to', DateTime, nullable=False),
    Column('message', Unicode(255), nullable=False),
    Column('trigger_type', SmallInteger, nullable=False),
    Column('trigger_list', Unicode(255), nullable=False),
    Column('price_rule', SmallInteger, nullable=False),
    Column('rule_value', Float(24), nullable=False),
    Column('stock_type', SmallInteger, nullable=False),
    Column('stock_list', Unicode(255), nullable=False),
    Column('pic_file', Unicode(100)),
    Column('max_selections', SmallInteger),
    Column('suggest_once', BIT),
    Column('inactive', BIT, nullable=False)
)


class Supplier(Base):
    __tablename__ = 'Supplier'
    __table_args__ = (
        Index('Custom2', 'custom2', 'supplier_id', unique=True),
        Index('Suburb', 'main_suburb', 'supplier_id', unique=True),
        Index('Position2', 'other_position', 'supplier_id', unique=True),
        Index('Custom1', 'custom1', 'supplier_id', unique=True),
        Index('Country', 'main_country', 'supplier_id', unique=True),
        Index('Position1', 'main_position', 'supplier_id', unique=True),
        Index('Supplier Name', 'supplier', 'supplier_id', unique=True),
        Index('Barcode', 'barcode', 'supplier_id', unique=True),
        Index('State', 'main_state', 'supplier_id', unique=True)
    )

    supplier_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    barcode = Column(Unicode(15), nullable=False, unique=True)
    supplier = Column(Unicode(50), nullable=False)
    grade = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    inactive = Column(BIT, nullable=False, server_default=text("(0)"))
    main_contact = Column(Unicode(50), nullable=False)
    main_position = Column(Unicode(50), nullable=False)
    main_addr1 = Column(Unicode(40), nullable=False)
    main_addr2 = Column(Unicode(40), nullable=False)
    main_addr3 = Column(Unicode(40), nullable=False)
    main_suburb = Column(Unicode(40), nullable=False)
    main_state = Column(Unicode(30), nullable=False)
    main_postcode = Column(Unicode(10), nullable=False)
    main_country = Column(Unicode(20), nullable=False)
    main_phone = Column(Unicode(20), nullable=False)
    main_fax = Column(Unicode(20), nullable=False)
    main_email = Column(Unicode(50), nullable=False)
    other_contact = Column(Unicode(50), nullable=False)
    other_position = Column(Unicode(50), nullable=False)
    other_addr1 = Column(Unicode(40), nullable=False)
    other_addr2 = Column(Unicode(40), nullable=False)
    other_addr3 = Column(Unicode(40), nullable=False)
    other_suburb = Column(Unicode(40), nullable=False)
    other_state = Column(Unicode(30), nullable=False)
    other_postcode = Column(Unicode(10), nullable=False)
    other_country = Column(Unicode(20), nullable=False)
    other_phone = Column(Unicode(20), nullable=False)
    other_fax = Column(Unicode(20), nullable=False)
    other_email = Column(Unicode(50), nullable=False)
    freight_free = Column(BIT, nullable=False, server_default=text("(0)"))
    reject_backorders = Column(BIT, nullable=False, server_default=text("(0)"))
    exported = Column(BIT, nullable=False, server_default=text("(0)"))
    date_modified = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    custom1 = Column(Unicode(50), nullable=False)
    custom2 = Column(Unicode(50), nullable=False)
    delivery_delay = Column(Integer, nullable=False, server_default=text("(0)"))
    abn = Column(Unicode(11), nullable=False)


t_Survey = Table(
    'Survey', metadata,
    Column('survey_id', Integer, nullable=False),
    Column('survey_name', Unicode(40), nullable=False),
    Column('inactive', BIT)
)


t_SurveyDocket = Table(
    'SurveyDocket', metadata,
    Column('docket_id', Integer, nullable=False),
    Column('survey_id', Integer, nullable=False),
    Column('item_id', Integer, nullable=False)
)


t_SurveyItem = Table(
    'SurveyItem', metadata,
    Column('item_id', Integer, nullable=False),
    Column('survey_id', Integer, nullable=False),
    Column('item_name', Unicode(40), nullable=False),
    Column('inactive', BIT)
)


t_SysInfo = Table(
    'SysInfo', metadata,
    Column('syskey', Unicode(20), nullable=False),
    Column('sysval', Unicode(255), nullable=False),
    Column('date_modified', DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
)


class TAWorking(Base):
    __tablename__ = 'TAWorking'

    salesorder_id = Column(Integer, primary_key=True)
    computer_user = Column(Unicode(60), nullable=False)
    start_time = Column(DateTime, nullable=False)
    ip = Column(Unicode(20), nullable=False)
    TA_number = Column(Unicode(40), nullable=False)
    staff_id = Column(Integer)


t_Tables = Table(
    'Tables', metadata,
    Column('table_id', Integer, nullable=False),
    Column('site_id', Integer, nullable=False),
    Column('table_code', Unicode(15), nullable=False),
    Column('table_status', SmallInteger, nullable=False),
    Column('seats', SmallInteger, nullable=False),
    Column('inactive', BIT, nullable=False),
    Column('staff_id', Integer),
    Column('logon_time', DateTime),
    Column('table_shape', SmallInteger),
    Column('table_left', SmallInteger),
    Column('table_top', SmallInteger),
    Column('table_width', SmallInteger),
    Column('table_height', SmallInteger),
    Column('show_state', SmallInteger),
    Column('table_fore_color', Integer),
    Column('table_font_size', SmallInteger),
    Column('state_fore_color', Integer),
    Column('state_font_size', SmallInteger),
    Column('customer_name', Unicode(60)),
    Column('table_left_rate', Float(24)),
    Column('table_top_rate', Float(24)),
    Column('table_width_rate', Float(24)),
    Column('table_height_rate', Float(24)),
    Column('computer_user', Unicode(100)),
    Column('start_time', DateTime),
    Column('ip', Unicode(20)),
    Column('kb_id', Integer)
)


t_TasteCat = Table(
    'TasteCat', metadata,
    Column('cat_id', Integer, nullable=False),
    Column('taste_id', Integer, nullable=False),
    Column('visible_type', SmallInteger)
)


t_TasteStock = Table(
    'TasteStock', metadata,
    Column('stock_id', Integer, nullable=False),
    Column('taste_id', Integer, nullable=False),
    Column('visible_type', SmallInteger)
)


class TaxCode(Base):
    __tablename__ = 'TaxCodes'

    code = Column(Unicode(3), primary_key=True)
    export = Column(Unicode(20), nullable=False, index=True)
    description = Column(Unicode(30), nullable=False)
    percentage = Column(Float(53), nullable=False, server_default=text("(0)"))
    tax_type = Column(SmallInteger, nullable=False, index=True, server_default=text("(0)"))
    sales_ac = Column(Unicode(31), nullable=False, index=True)
    goods_ac = Column(Unicode(31), nullable=False, index=True)
    date_modified = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))


t_TempSales = Table(
    'TempSales', metadata,
    Column('stock_id', Float(53), nullable=False),
    Column('quantity', Float(53), nullable=False)
)


t_TextPrinters = Table(
    'TextPrinters', metadata,
    Column('printer', Unicode(80), nullable=False),
    Column('printer2', Unicode(80), nullable=False),
    Column('cutter', Unicode(100)),
    Column('dw_on', Unicode(100)),
    Column('dw_off', Unicode(100)),
    Column('color_on', Unicode(100)),
    Column('color_off', Unicode(100)),
    Column('printer_cols', SmallInteger),
    Column('thermal_printer', BIT)
)


t_Till = Table(
    'Till', metadata,
    Column('drawer', Unicode(1), nullable=False),
    Column('drawer_name', Unicode(30), nullable=False),
    Column('ip_addr', Unicode(20)),
    Column('inactive', BIT, nullable=False)
)


t_TimePeriod = Table(
    'TimePeriod', metadata,
    Column('time_id', Integer, nullable=False),
    Column('time_code', Unicode(15), nullable=False),
    Column('time_name', Unicode(20), nullable=False),
    Column('time_name2', Unicode(20), nullable=False),
    Column('inactive', BIT, nullable=False),
    Column('start_time', DateTime),
    Column('kb_id', Integer),
    Column('auto_kb', BIT),
    Column('price_level', Integer),
    Column('auto_price', BIT),
    Column('end_time', DateTime),
    Column('cutoff_time', Float(53))
)


t_TimePeriodCat = Table(
    'TimePeriodCat', metadata,
    Column('cat_id', Integer, nullable=False),
    Column('time_id', Integer, nullable=False),
    Column('price_level', SmallInteger),
    Column('inactive', BIT),
    Column('date_modified', DateTime)
)


t_TimePeriodStock = Table(
    'TimePeriodStock', metadata,
    Column('stock_id', Integer, nullable=False),
    Column('time_id', Integer, nullable=False),
    Column('price_level', SmallInteger),
    Column('inactive', BIT),
    Column('date_modified', DateTime)
)


t_Urging = Table(
    'Urging', metadata,
    Column('line_id', Integer, nullable=False),
    Column('table_code', Unicode(20), nullable=False),
    Column('staff_name', Unicode(40), nullable=False),
    Column('cat1', Unicode(20), nullable=False),
    Column('description', Unicode(60)),
    Column('description2', Unicode(60)),
    Column('unit', Unicode(10), nullable=False),
    Column('quantity', Float(24), nullable=False),
    Column('printer', Unicode(60), nullable=False),
    Column('printer2', Unicode(60), nullable=False),
    Column('order_time', DateTime, nullable=False),
    Column('print_type', SmallInteger, nullable=False)
)


t_UrgingMsg = Table(
    'UrgingMsg', metadata,
    Column('message_code', Unicode(10), nullable=False),
    Column('message', Unicode(40), nullable=False)
)


t_Working = Table(
    'Working', metadata,
    Column('licence', SmallInteger, nullable=False),
    Column('terminal', Unicode(40), nullable=False)
)


class Customer(Base):
    __tablename__ = 'Customer'
    __table_args__ = (
        Index('State', 'state', 'customer_id', unique=True),
        Index('Suburb', 'suburb', 'customer_id', unique=True),
        Index('Customer Name', 'surname', 'given_names', 'customer_id', unique=True),
        Index('Country', 'country', 'customer_id', unique=True),
        Index('Company', 'company', 'customer_id', unique=True),
        Index('Custom2', 'custom2', 'customer_id', unique=True),
        Index('Given Names', 'given_names', 'customer_id', unique=True),
        Index('Custom1', 'custom1', 'customer_id', unique=True),
        Index('Salutation', 'salutation', 'customer_id', unique=True),
        Index('Surname', 'surname', 'customer_id', unique=True),
        Index('Position', 'position', 'customer_id', unique=True),
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


class GlobalSettingSub(Base):
    __tablename__ = 'GlobalSettingSub'

    setting_key = Column(ForeignKey('GlobalSetting.setting_key'), primary_key=True, nullable=False)
    setting_subkey = Column(Unicode(50), primary_key=True, nullable=False)
    setting_value = Column(Unicode(3000))

    GlobalSetting = relationship('GlobalSetting')


class Good(Base):
    __tablename__ = 'Goods'

    goods_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    goods_date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    staff_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    supplier_id = Column(ForeignKey('Supplier.supplier_id'), nullable=False, index=True, server_default=text("(0)"))
    invoice_no = Column(Unicode(20), nullable=False, index=True)
    invoice_date = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    order_no = Column(Unicode(20), nullable=False, index=True)
    order_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    comments = Column(Unicode(255), nullable=False)
    exported = Column(BIT, nullable=False, server_default=text("(0)"))
    subtotal_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    subtotal_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    freight_tax = Column(Unicode(3), nullable=False)
    freight_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    freight_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    total_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    total_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    expected = Column(MONEY, nullable=False, server_default=text("(0)"))
    days = Column(SmallInteger)

    supplier = relationship('Supplier')


class Order(Base):
    __tablename__ = 'Orders'

    order_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    revision = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    order_date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    due_date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    staff_id = Column(ForeignKey('Staff.staff_id'), nullable=False, index=True, server_default=text("(0)"))
    supplier_id = Column(ForeignKey('Supplier.supplier_id'), nullable=False, index=True, server_default=text("(0)"))
    order_suffix = Column(Unicode(15), nullable=False)
    comments = Column(Unicode(255), nullable=False)
    archive = Column(BIT, nullable=False, server_default=text("(0)"))

    staff = relationship('Staff')
    supplier = relationship('Supplier')


class Return(Base):
    __tablename__ = 'Returns'

    returns_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    returns_date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    staff_id = Column(ForeignKey('Staff.staff_id'), nullable=False, index=True, server_default=text("(0)"))
    supplier_id = Column(ForeignKey('Supplier.supplier_id'), nullable=False, index=True, server_default=text("(0)"))
    ra_no = Column(Unicode(20), nullable=False)
    comments = Column(Unicode(255), nullable=False)
    exported = Column(BIT, nullable=False, server_default=text("(0)"))
    freight_tax = Column(Unicode(3), nullable=False)
    freight_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    freight_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    total_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    total_inc = Column(MONEY, nullable=False, server_default=text("(0)"))

    staff = relationship('Staff')
    supplier = relationship('Supplier')


class SalesOrderLineBackup(Base):
    __tablename__ = 'SalesOrderLineBackup'
    __table_args__ = (
        ForeignKeyConstraint(['salesorder_id', 'terminal_name', 'backup_time'], ['SalesOrderBackup.salesorder_id', 'SalesOrderBackup.terminal_name', 'SalesOrderBackup.backup_time']),
    )

    line_id = Column(Integer, primary_key=True, nullable=False)
    salesorder_id = Column(Integer, nullable=False)
    stock_id = Column(Float(53), nullable=False)
    cost_ex = Column(MONEY, nullable=False)
    cost_inc = Column(MONEY, nullable=False)
    sales_tax = Column(Unicode(3), nullable=False)
    sell_ex = Column(MONEY, nullable=False)
    sell_inc = Column(MONEY, nullable=False)
    rrp = Column(MONEY, nullable=False)
    print_ex = Column(MONEY, nullable=False)
    print_inc = Column(MONEY, nullable=False)
    quantity = Column(Float(53), nullable=False)
    parentline_id = Column(Integer, nullable=False)
    package = Column(BIT, nullable=False)
    status = Column(SmallInteger, nullable=False)
    orderline_id = Column(Integer, nullable=False)
    size_level = Column(SmallInteger)
    staff_id = Column(Integer)
    time_ordered = Column(DateTime)
    out_order = Column(SmallInteger)
    hand_writting = Column(BIT)
    seq_id = Column(Integer)
    original_line_id = Column(Integer)
    backup_time = Column(DateTime, primary_key=True, nullable=False)
    terminal_name = Column(Unicode(50), primary_key=True, nullable=False)
    backup_id = Column(Integer)

    salesorder = relationship('SalesOrderBackup')


class SalesOrderLineSPO(Base):
    __tablename__ = 'SalesOrderLineSPO'

    line_id = Column(Integer, primary_key=True)
    salesorder_id = Column(ForeignKey('SalesOrderSPO.salesorder_id'), nullable=False)
    stock_id = Column(Float(53), nullable=False)
    cost_ex = Column(MONEY, nullable=False)
    cost_inc = Column(MONEY, nullable=False)
    sales_tax = Column(Unicode(3), nullable=False)
    sell_ex = Column(MONEY, nullable=False)
    sell_inc = Column(MONEY, nullable=False)
    rrp = Column(MONEY, nullable=False)
    print_ex = Column(MONEY, nullable=False)
    print_inc = Column(MONEY, nullable=False)
    quantity = Column(Float(53), nullable=False)
    parentline_id = Column(Integer, nullable=False)
    package = Column(BIT, nullable=False)
    status = Column(SmallInteger, nullable=False)
    orderline_id = Column(Integer, nullable=False)
    size_level = Column(SmallInteger)
    staff_id = Column(Integer)
    time_ordered = Column(DateTime)
    out_order = Column(SmallInteger)
    hand_writting = Column(BIT)
    seq_id = Column(Integer)
    original_line_id = Column(Integer)

    salesorder = relationship('SalesOrderSPO')


class Stock(Base):
    __tablename__ = 'Stock'
    __table_args__ = (
        Index('Custom1', 'custom1', 'stock_id', unique=True),
        Index('Description', 'description', 'stock_id', unique=True),
        Index('Sub', 'cat2', 'stock_id', unique=True),
        Index('Custom2', 'custom2', 'stock_id', unique=True),
        Index('Bar code', 'barcode', 'stock_id', unique=True),
        Index('Supplier', 'supplier_id', 'stock_id', unique=True),
        Index('Cat', 'cat1', 'stock_id', unique=True),
        Index('Categories', 'cat1', 'cat2', 'stock_id', unique=True)
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
    sell5 = Column(MONEY)
    sell6 = Column(MONEY)
    sell7 = Column(MONEY)
    sell8 = Column(MONEY)

    supplier = relationship('Supplier')


class PricingStock(Stock):
    __tablename__ = 'Pricing_Stock'

    stock_id = Column(ForeignKey('Stock.stock_id'), primary_key=True, unique=True, server_default=text("(0)"))
    DefaultRule = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    RuleA = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    RuleB = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    RuleC = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    RuleD = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    DefaultValue = Column(Float(53), nullable=False, server_default=text("(0)"))
    ValueA = Column(Float(53), nullable=False, server_default=text("(0)"))
    ValueB = Column(Float(53), nullable=False, server_default=text("(0)"))
    ValueC = Column(Float(53), nullable=False, server_default=text("(0)"))
    ValueD = Column(Float(53), nullable=False, server_default=text("(0)"))
    date_modified = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    date_from = Column(DateTime)
    date_to = Column(DateTime)


class Audit(Base):
    __tablename__ = 'Audit'

    audit_date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    audit_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    source_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    tran_type = Column(Unicode(2), nullable=False, index=True)
    stock_id = Column(ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)"))
    movement = Column(Float(53), nullable=False, server_default=text("(0)"))
    stock_value = Column(MONEY, nullable=False, server_default=text("(0)"))
    exported = Column(BIT, nullable=False, server_default=text("(0)"))
    current_qty = Column(Float(24))

    stock = relationship('Stock')


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


class GoodsLine(Base):
    __tablename__ = 'GoodsLine'

    line_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    goods_id = Column(ForeignKey('Goods.goods_id'), nullable=False, index=True, server_default=text("(0)"))
    stock_id = Column(ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)"))
    goods_tax = Column(Unicode(3), nullable=False)
    cost_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    cost_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    sell = Column(MONEY, nullable=False, server_default=text("(0)"))
    quantity = Column(Float(53), nullable=False, server_default=text("(0)"))
    expire_date = Column(DateTime)
    print_ex = Column(MONEY)
    print_inc = Column(MONEY)
    item_disc = Column(MONEY)

    goods = relationship('Good')
    stock = relationship('Stock')


class Layby(Base):
    __tablename__ = 'Layby'

    layby_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    layby_date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    expiry_date = Column(DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
    staff_id = Column(ForeignKey('Staff.staff_id'), nullable=False, index=True, server_default=text("(0)"))
    original_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    customer_id = Column(ForeignKey('Customer.customer_id'), nullable=False, index=True, server_default=text("(0)"))
    custom = Column(Unicode(20), nullable=False)
    comments = Column(Unicode(255), nullable=False)
    closed = Column(BIT, nullable=False, server_default=text("(0)"))
    subtotal = Column(MONEY, nullable=False, server_default=text("(0)"))
    discount = Column(MONEY, nullable=False, server_default=text("(0)"))
    rounding = Column(MONEY, nullable=False, server_default=text("(0)"))
    total_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    total_inc = Column(MONEY, nullable=False, server_default=text("(0)"))

    customer = relationship('Customer')
    staff = relationship('Staff')


class OrdersLine(Base):
    __tablename__ = 'OrdersLine'

    line_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    order_id = Column(ForeignKey('Orders.order_id'), nullable=False, index=True, server_default=text("(0)"))
    supplier_id = Column(ForeignKey('Supplier.supplier_id'), nullable=False, index=True, server_default=text("(0)"))
    stock_id = Column(ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)"))
    supcode = Column(Unicode(16), nullable=False)
    cost_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    cost_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    goods_tax = Column(Unicode(3), nullable=False)
    quantity = Column(Float(53), nullable=False, server_default=text("(0)"))
    status = Column(SmallInteger, nullable=False, server_default=text("(0)"))
    goods_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    print_ex = Column(MONEY)
    print_inc = Column(MONEY)
    item_disc = Column(MONEY)

    order = relationship('Order')
    stock = relationship('Stock')
    supplier = relationship('Supplier')


t_Package = Table(
    'Package', metadata,
    Column('package_id', ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)")),
    Column('stock_id', ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)")),
    Column('sell_inc', MONEY, nullable=False, server_default=text("(0)")),
    Column('quantity', Float(53), nullable=False, server_default=text("(0)")),
    Column('date_modified', DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')")),
    Column('sell_inc2', MONEY),
    Column('sell_inc3', MONEY),
    Column('sell_inc4', MONEY)
)


class ReturnsLine(Base):
    __tablename__ = 'ReturnsLine'

    line_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    returns_id = Column(ForeignKey('Returns.returns_id'), nullable=False, index=True, server_default=text("(0)"))
    stock_id = Column(ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)"))
    cost_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    cost_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    goods_tax = Column(Unicode(3), nullable=False)
    invoice_no = Column(Unicode(20), nullable=False, index=True)
    quantity = Column(Float(53), nullable=False, server_default=text("(0)"))

    returns = relationship('Return')
    stock = relationship('Stock')


class SalesOrder(Base):
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


t_StockTake = Table(
    'StockTake', metadata,
    Column('stocktake_date', DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')")),
    Column('stock_id', ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)")),
    Column('quantity', Float(53), nullable=False, server_default=text("(0)")),
    Column('date_modified', DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')")),
    Column('current_qty', Float(24))
)


t_SupplierCode = Table(
    'SupplierCode', metadata,
    Column('supcode', Unicode(16), nullable=False, index=True),
    Column('supplier_id', ForeignKey('Supplier.supplier_id'), nullable=False, index=True, server_default=text("(0)")),
    Column('stock_id', ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)")),
    Column('date_modified', DateTime, nullable=False, server_default=text("('9/24/2003 1:47:12')"))
)


class CashupSession(Base):
    __tablename__ = 'Cashup_Sessions'

    session_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    staff_id = Column(ForeignKey('Staff.staff_id'), nullable=False, index=True, server_default=text("(0)"))
    session_date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    docket_id = Column(ForeignKey('Docket.docket_id'), nullable=False, index=True, server_default=text("(0)"))
    drawer = Column(Unicode(1), nullable=False, index=True)
    status = Column(SmallInteger, nullable=False, index=True, server_default=text("(0)"))
    comments = Column(Unicode(255), nullable=False)
    stock_value = Column(MONEY, nullable=False, server_default=text("(0)"))
    stock_variance = Column(MONEY, nullable=False, server_default=text("(0)"))
    exportation_state = Column(SmallInteger, nullable=False, server_default=text("(0)"))

    docket = relationship('Docket')
    staff = relationship('Staff')


class CreditNote(Base):
    __tablename__ = 'CreditNotes'

    credit_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    credit_date = Column(DateTime, nullable=False, index=True, server_default=text("('9/24/2003 1:47:12')"))
    note_id = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    docket_id = Column(ForeignKey('Docket.docket_id'), nullable=False, index=True, server_default=text("(0)"))
    amount = Column(MONEY, nullable=False, server_default=text("(0)"))
    customer_id = Column(ForeignKey('Customer.customer_id'), nullable=False, index=True, server_default=text("(0)"))
    credit_type = Column(Integer, nullable=False, server_default=text("(0)"))

    customer = relationship('Customer')
    docket = relationship('Docket')


class DocketAddres(Base):
    __tablename__ = 'DocketAddress'

    line_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    docket_id = Column(ForeignKey('Docket.docket_id'), nullable=False, unique=True, server_default=text("(0)"))
    customer_id = Column(ForeignKey('Customer.customer_id'), nullable=False, index=True, server_default=text("(0)"))
    addr1 = Column(Unicode(40), nullable=False)
    addr2 = Column(Unicode(40), nullable=False)
    addr3 = Column(Unicode(40), nullable=False)
    suburb = Column(Unicode(40), nullable=False)
    state = Column(Unicode(30), nullable=False)
    postcode = Column(Unicode(10), nullable=False)
    country = Column(Unicode(20), nullable=False)
    phone = Column(Unicode(20), nullable=False)
    delivery_date = Column(Unicode(15), nullable=False)

    customer = relationship('Customer')
    docket = relationship('Docket')


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


class DocketDesc(DocketLine):
    __tablename__ = 'DocketDesc'

    line_id = Column(ForeignKey('DocketLine.line_id'), primary_key=True, unique=True, server_default=text("(0)"))
    description = Column(Unicode(200))


class DocketPackage(Base):
    __tablename__ = 'DocketPackages'

    line_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    min_line = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    max_line = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    docket_id = Column(ForeignKey('Docket.docket_id'), nullable=False, index=True, server_default=text("(0)"))
    customer_id = Column(ForeignKey('Customer.customer_id'), nullable=False, index=True, server_default=text("(0)"))
    package_id = Column(ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)"))
    sales_tax = Column(Unicode(3), nullable=False)
    cost_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    cost_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    sell_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    sell_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    rrp = Column(MONEY, nullable=False, server_default=text("(0)"))
    print_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    print_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    quantity = Column(Float(53), nullable=False, server_default=text("(0)"))
    gp = Column(MONEY, nullable=False, server_default=text("(0)"))

    customer = relationship('Customer')
    docket = relationship('Docket')
    package = relationship('Stock')


class LaybyAddres(Base):
    __tablename__ = 'LaybyAddress'

    line_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    layby_id = Column(ForeignKey('Layby.layby_id'), nullable=False, unique=True, server_default=text("(0)"))
    customer_id = Column(ForeignKey('Customer.customer_id'), nullable=False, index=True, server_default=text("(0)"))
    addr1 = Column(Unicode(40), nullable=False)
    addr2 = Column(Unicode(40), nullable=False)
    addr3 = Column(Unicode(40), nullable=False)
    suburb = Column(Unicode(40), nullable=False)
    state = Column(Unicode(30), nullable=False)
    postcode = Column(Unicode(10), nullable=False)
    country = Column(Unicode(20), nullable=False)
    phone = Column(Unicode(20), nullable=False)
    delivery_date = Column(Unicode(15), nullable=False)

    customer = relationship('Customer')
    layby = relationship('Layby')


class LaybyLine(Base):
    __tablename__ = 'LaybyLine'

    line_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    layby_id = Column(ForeignKey('Layby.layby_id'), nullable=False, index=True, server_default=text("(0)"))
    stock_id = Column(ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)"))
    cost_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    cost_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    sales_tax = Column(Unicode(3), nullable=False)
    sell_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    sell_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    rrp = Column(MONEY, nullable=False, server_default=text("(0)"))
    print_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    print_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    customer_id = Column(ForeignKey('Customer.customer_id'), nullable=False, index=True, server_default=text("(0)"))
    quantity = Column(Float(53), nullable=False, server_default=text("(0)"))
    package_id = Column(Float(53), nullable=False, index=True, server_default=text("(0)"))

    customer = relationship('Customer')
    layby = relationship('Layby')
    stock = relationship('Stock')


class LaybyDesc(LaybyLine):
    __tablename__ = 'LaybyDesc'

    line_id = Column(ForeignKey('LaybyLine.line_id'), primary_key=True, unique=True, server_default=text("(0)"))
    description = Column(Unicode(40), nullable=False)


class LaybyPackage(Base):
    __tablename__ = 'LaybyPackages'

    line_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    min_line = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    max_line = Column(Integer, nullable=False, index=True, server_default=text("(0)"))
    layby_id = Column(ForeignKey('Layby.layby_id'), nullable=False, index=True, server_default=text("(0)"))
    customer_id = Column(ForeignKey('Customer.customer_id'), nullable=False, index=True, server_default=text("(0)"))
    package_id = Column(ForeignKey('Stock.stock_id'), nullable=False, index=True, server_default=text("(0)"))
    cost_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    cost_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    rrp = Column(MONEY, nullable=False, server_default=text("(0)"))
    sales_tax = Column(Unicode(3), nullable=False)
    sell_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    sell_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    print_ex = Column(MONEY, nullable=False, server_default=text("(0)"))
    print_inc = Column(MONEY, nullable=False, server_default=text("(0)"))
    quantity = Column(Float(53), nullable=False, server_default=text("(0)"))

    customer = relationship('Customer')
    layby = relationship('Layby')
    package = relationship('Stock')


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


class SalesOrderAddres(Base):
    __tablename__ = 'SalesOrderAddress'

    line_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    salesorder_id = Column(ForeignKey('SalesOrder.salesorder_id'), nullable=False, unique=True, server_default=text("(0)"))
    addr1 = Column(Unicode(40), nullable=False)
    addr2 = Column(Unicode(40), nullable=False)
    addr3 = Column(Unicode(40), nullable=False)
    suburb = Column(Unicode(40), nullable=False)
    state = Column(Unicode(30), nullable=False)
    postcode = Column(Unicode(10), nullable=False)
    country = Column(Unicode(20), nullable=False)
    phone = Column(Unicode(20), nullable=False)
    delivery_date = Column(Unicode(15), nullable=False)

    salesorder = relationship('SalesOrder')


class SalesOrderLine(Base):
    __tablename__ = 'SalesOrderLine'

    line_id = Column(Integer, primary_key=True, server_default=text("(0)"))
    salesorder_id = Column(ForeignKey('SalesOrder.salesorder_id'), nullable=False, index=True, server_default=text("(0)"))
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
    points = Column(Integer)

    salesorder = relationship('SalesOrder')
    stock = relationship('Stock')


class SalesOrderDesc(SalesOrderLine):
    __tablename__ = 'SalesOrderDesc'

    line_id = Column(ForeignKey('SalesOrderLine.line_id'), primary_key=True, unique=True, server_default=text("(0)"))
    description = Column(Unicode(200))


t_Cashup_Shortages = Table(
    'Cashup_Shortages', metadata,
    Column('shortage_id', Integer, nullable=False, server_default=text("(0)")),
    Column('session_id', ForeignKey('Cashup_Sessions.session_id'), nullable=False, index=True, server_default=text("(0)")),
    Column('paymenttype', Unicode(15), nullable=False, index=True),
    Column('amount', MONEY, nullable=False, server_default=text("(0)")),
    Column('exported', BIT, nullable=False, server_default=text("(0)")),
    Column('counted', MONEY)
)
