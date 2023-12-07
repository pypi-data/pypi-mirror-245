import datetime


class Contact:
    name: str
    tel: str

    def __init__(self, name, tel):
        self.name = name
        self.tel = tel

    def __repr__(self) -> str:
        return f"name:{self.name} tel:{self.tel}"


class CheckMan:
    id: str
    name: str

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f"id:{self.id} name:{self.name}"


class ReportData:
    reportFullId: str = ""  # 报告编号
    checkedCompanyName: str = ""  # 受检单位
    projName: str = ""  # 项目名称
    checkType: str = ""  # 检测类别
    projContact: Contact = None  # 联系人
    proofLevel: str = ""  # 防雷类别
    validStartDate: datetime.date = None  # 报告有效期开始
    validEndDate: datetime.date = None  # 报告有效期截至
    checkDate: datetime.date = None  # 检测日期
    projAddr: str = ""  # 项目地址
    reportResult: str = ""  # 检测结论
    checkedUnitCount: int = 0  # 检测数量
    checkMans: [CheckMan] = []  # 检测人员
    checkPointCount: int = 0  # 点数

    def toString(self):
        return f"报告编号={self.reportFullId}\n" \
               f"受检单位={self.checkedCompanyName}\n" \
               f"项目名称={self.projName}\n" \
               f"检测类别={self.checkType}\n" \
               f"联系人={self.projContact}\n" \
               f"防雷类别={self.proofLevel}\n" \
               f"报告有效期开始={self.validStartDate}\n" \
               f"报告有效期截至={self.validEndDate}\n" \
               f"检测日期={self.checkDate}\n" \
               f"项目地址={self.projAddr}\n" \
               f"检测结论={self.reportResult}\n" \
               f"检测数量={self.checkedUnitCount}\n" \
               f"检测人员={self.checkMans}\n" \
               f"点数={self.checkPointCount}\n"
