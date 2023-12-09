# -*- coding: utf-8 -*-
import calendar
import datetime


class Date:
    @classmethod
    def today(cls) -> datetime.date:
        return datetime.datetime.now().date()

    @classmethod
    def first_day_of_month(cls, date: datetime.date = None) -> datetime.date:
        """获取本月1日"""
        date = date or cls.today()
        return date.replace(day=1)

    @classmethod
    def last_day_of_month(cls, date: datetime.date = None) -> datetime.date:
        """获取本月最后1日"""
        date = date or cls.today()
        days_in_month: int = calendar.monthrange(date.year, date.month)[1]
        return date.replace(day=days_in_month)

    @classmethod
    def first_day_of_next_month(cls, date: datetime.date = None) -> datetime.date:
        """获取下个月第一日"""
        date = date or cls.today()
        return cls.last_day_of_month(date=date) + datetime.timedelta(days=1)

    @classmethod
    def last_day_of_next_month(cls, date: datetime.date = None) -> datetime.date:
        """获取下个月最后一日"""
        date = date or cls.today()
        date = cls.first_day_of_next_month(date=date)
        days_in_month: int = calendar.monthrange(date.year, date.month)[1]
        return date.replace(day=days_in_month)

    @classmethod
    def first_day_of_previous_month(cls, date: datetime.date = None) -> datetime.date:
        """获取上个月第一日"""
        date = date or cls.today()
        date = cls.last_day_of_previous_month(date=date)
        return cls.first_day_of_month(date=date)

    @classmethod
    def last_day_of_previous_month(cls, date: datetime.date = None) -> datetime.date:
        """获取上个月最后一日"""
        date = date or cls.today()
        return cls.first_day_of_month(date=date) - datetime.timedelta(days=1)
