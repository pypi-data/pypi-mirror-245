import datetime


class Contact:
    def __init__(self, name, tel):
        self.name = name
        self.tel = tel

    def __repr__(self) -> str:
        return f"name:{self.name} tel:{self.tel}"


class CheckMan:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f"id:{self.id} name:{self.name}"


class ReportData:
    def __init__(self):
        self.reportFullId: str = ""  # 完整报告编号
        self.reportShortId: str = ""  # 短报告编号
        self.checkedCompanyName: str = ""  # 受检单位
        self.projName: str = ""  # 项目名称
        self.checkType: str = ""  # 检测类别
        self.projContact: Contact = None  # 联系人
        self.proofLevel: str = ""  # 防雷类别
        self.validStartDate: datetime.date = None  # 报告有效期开始
        self.validEndDate: datetime.date = None  # 报告有效期截至
        self.checkDate: datetime.date = None  # 检测日期
        self.projAddr: str = ""  # 项目地址
        self.reportResult: str = ""  # 检测结论
        self.checkedUnitCount: int = 0  # 检测数量
        self.checkMans: [CheckMan] = []  # 检测人员
        self.checkPointCount: int = 0  # 点数

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
