import tornado.web
import calendar
import datetime

class CalModule(tornado.web.UIModule):
    def render(self, dt):
        cal = MyCalendar(calendar.SUNDAY).formatmonth(dt.year, dt.month)
        return cal.replace(u"<td><a href=\"./-%d\">"%dt.day, u"<td class=\"active\"><a href=\"./-%d\">"%dt.day)

class FileSizeModule(tornado.web.UIModule):
    def render(self, size):
        try:
            size = float(size)
        except (TypeError,ValueError,UnicodeDecodeError):
            return u"0 B"
        KB = 1<<10
        MB = 1<<20
        GB = 1<<30
        if size < KB:
            return str(size)+' B'
        elif size < MB:
            return str(round(size/KB,1))+' K'
        elif size < GB:
            return str(round(size/MB,1))+' M'
        else:
            return str(round(size/GB,1))+' G'

class MyCalendar(calendar.HTMLCalendar):
    def lastmonth(self, theyear, themonth):
        first = datetime.date(day=1, month=themonth, year=theyear)
        lastMonth = first - datetime.timedelta(days=1)
        return lastMonth.strftime("/log/%Y-%m/-%d")
    def nextmonth(self, theyear, themonth):
        last = datetime.date(day=calendar.mdays[themonth], month=themonth, year=theyear)
        nextMonth = last + datetime.timedelta(days=1)
        return nextMonth.strftime("/log/%Y-%m/-%d")

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="out">&nbsp;</td>' # day outside month
        else:
            return '<td><a href="./-%d">%d</a></td>' % (day, day)

    def formatweek(self, theweek):
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatweekday(self, day):
        return '<th>%s</th>' % calendar.day_abbr[day]

    def formatweekheader(self):
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        return '<thead><tr>%s</tr></thead>' % s

    def formatmonthname(self, theyear, themonth, withyear=True):
        if withyear:
            s = '%s %s' % (calendar.month_name[themonth], theyear)
        else:
            s = '%s' % calendar.month_name[themonth]
        return '<caption>\
<span class="prev"><a href=%s>&larr;</a></span>\
<span class="next"><a href=%s>&rarr;</a></span>\
%s</caption>' % (self.lastmonth(theyear, themonth),self.nextmonth(theyear, themonth),s)

    def formatmonth(self, theyear, themonth, withyear=True):
        v = []
        a = v.append
        a('<table class="cal">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)