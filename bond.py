# -*- coding: utf-8 -*-

import sys
sys.path.append(r'C:\Users\70242\Documents\Python\用python帮做作业')
#from bond import Bond

AUTHOR = 'Michael Wang'

class Bond():
    '''Standard type of bond, with fixed maturity and coupon rate.
    Able to elapse certain number of years, to see how bond changes
    when time passing by.  
    
    `updated 2018/10/14`

    Parameters
    ----------

    maturity : the time remains for the bond to mature.  
        Must spoecify explicitly.

    par : the par value of the bond.  
        Default is 100.

    coupon : the coupon rate of the bond.  
        Default is 0.

    freq : the frequency of interst payment.  
        Default is 1.

    YTM : the Yield to Maturity, or the Required Rate of Return, 
        or the Market Capitalization Rate.  
        It can be a given parameter, or be calculated automatically.  
        In some cases, if the given YTM does not equal that is calculated, 
        it will raise a warning, and use the calculated one instead.

    Examples
    --------

    >>> bond = Bond(maturity=18, par=1000, price=1169, coupon=0.11, freq=2,
                    putPrice=1000, putYear=5, callPrice=1055, callYear=8)
    >>> bond.info  
     - - - - - - - - - - - - - - - - - - - - -
    |                 B O N D                 |
    |         Issued by Michael Wang          |
    | Par Value: 1000      Coupon Rate: 11.0% |
    | Maturity: 18        Payment Freqency: 2 |
    | Yeild to Maturity: 9.0769%              |
    | Price: 1169.00                          |
    |                                         |
    | MacaulayDuration   :           10.36149 |
    | ModifiedDuration   :            9.91166 |
    | DollarDuration     :        -9911.65886 |
    | Convexity:         :          128.56799 |
    |                                         |
    | Yeild to Put: 6.942% (in 5 years)       |
    | Yeild to Call: 8.535% (in 8 years)      |
    - - - - - - - - - - - - - - - - - - - - -
    '''

    def __init__(self, maturity, coupon=0, freq=1, par=100, **arg):
        self.maturity = maturity
        self.par = par
        self.coupon = coupon
        self.freq = freq

        YTM = arg.pop("YTM", None)
        price = arg.pop("price", None)
        if YTM is None and price is None:
            raise ValueError("You must enter either 'Price' or 'Yield to Maturity'.")
        if not(YTM is None):
            self.YTM = YTM
        else:
            self.price = price
            self._YTM = None

        self.putPrice = arg.pop("putPrice", None)
        self.putYear = arg.pop("putYear", None)
        self.putable = not((self.putPrice is None) or (self.putYear is None))

        self.callPrice = arg.pop("callPrice", None)
        self.callYear = arg.pop("callYear", None)
        self.callable = not((self.callPrice is None) or (self.callYear is None))

    @property
    def info(self):
        '''
        A quick review of the bond.
        '''
        self.duration

        print(' -'*21)
        print('| {:^39} |'.format('B O N D'))
        print('| {:^39} |'.format('Issued by %s' % AUTHOR))

        print('| {:<19}{:>20} |'.format('Par Value: %d' % self.par, 
                                        'Coupon Rate: {:.1%}'.format(self.coupon)))
        print('| {:<19}{:>20} |'.format('Maturity: %d' % self.maturity, 
                                        'Payment Freqency: {}'.format(self.freq)))
        print('| {:<39} |'.format('Yeild to Maturity: {:.4%}'.format(self.YTM)))
        print('| {:<39} |'.format('Price: {:.2f}'.format(self.price)))
        print('|', ' '*39, '|')
        print('| {:<19}: {:>18} |\n| {:<19}: {:>18} |\n| {:<19}: {:>18} |'
              .format('MacaulayDuration', '%9.5f' % self.MacaulayDuration,
                      'ModifiedDuration', '%9.5f' % self.ModifiedDuration,
                      'DollarDuration', '%9.5f' % self.DollarDuration))
        print('| {:<19}: {:>18} |'.format('Convexity: ', '%9.5f' % self.convexity))

        if self.putable:
            print('|', ' '*39, '|')
            print('| {:<39} |'.format('Yeild to Put: {:.3%} (in {} years)'.format(self.YTP, self.putYear)))

        if self.callable:
            print('| {:<39} |'.format('Yeild to Call: {:.3%} (in {} years)'.format(self.YTC, self.callYear)))

        print(' -'*21)
        print()

    @classmethod
    def bondPrice(self, coupon, maturity, freq, YTM):
        n = maturity * freq
        rate = YTM/freq
        return PVCF(rate, n) * (coupon / freq) + PVM(rate, n)

    @property
    def YTM(self):
        '''
        Binary search for the solution.
        '''
        if self._YTM is None:
            accuracy = 1e-4
            low = 0
            high = 0.5
            p_mid = 0
            while abs(self.price - p_mid) > accuracy:
                mid = (high + low) / 2
                p_high = self.bondPrice(
                    self.coupon, self.maturity, self.freq, low) * self.par
                p_low = self.bondPrice(
                    self.coupon, self.maturity, self.freq, high) * self.par
                p_mid = self.bondPrice(
                    self.coupon, self.maturity, self.freq, mid) * self.par
                # print(p_high, p_low)
                if (self.price < p_high) and (self.price > p_mid):
                    high = mid
                elif (self.price > p_low) and (self.price < p_mid):
                    low = mid
            self._YTM = mid
            return self._YTM
        # If YTM already exists, return it directly
        return self._YTM

    @YTM.setter
    def YTM(self, YTM_Given):
        '''
        Need to check if the given YTM is correnct.
        '''
        if YTM_Given >= 0:
            self._YTM = YTM_Given
        # Calculate bond price with given YTM
        self.price = self.bondPrice(self.coupon, self.maturity, self.freq, self._YTM) * self.par

    @property
    def duration(self):
        n = self.maturity * self.freq
        y = self.YTM/self.freq
        C = self.par * (self.coupon / self.freq)
        temp = n * self.par * PVM(y, n)
        for t in range(1, n+1):
            temp += t * C / (1 + y)**t

        self.MacaulayDuration = temp / self.par / self.freq
        self.ModifiedDuration = self.MacaulayDuration / (1 + y)
        self.DollarDuration = - self.ModifiedDuration * self.par

        return dict(MacaulayDuration=self.MacaulayDuration,
                    ModifiedDuration=self.ModifiedDuration,
                    DollarDuration=self.DollarDuration)

    @property
    def convexity(self):
        n = self.maturity * self.freq
        y = self.YTM / self.freq
        C = self.par * (self.coupon / self.freq)
        temp = n * (n+1) * self.par * PVM(y, n+2)
        for t in range(1, n+1):
            temp += t * (t + 1) * C / (1 + y)**(t+2)
        return temp / self.par / self.freq**2

    @property
    def YTP(self):
        if not self.putable:
            return None
        n = self.putYear * self.freq
        C = self.par * (self.coupon / self.freq)

        accuracy = 1e-4
        low = 0
        high = 1
        p_mid = 0
        while abs(self.price - p_mid) > accuracy:
            mid = (high + low) / 2
            p_high = C * PVCF(low, n) + self.putPrice * PVM(low, n)
            p_low = C * PVCF(high, n) + self.putPrice * PVM(high, n)
            p_mid = C * PVCF(mid, n) + self.putPrice * PVM(mid, n)
            if (self.price < p_high) and (self.price > p_mid):
                high = mid
            elif (self.price > p_low) and (self.price < p_mid):
                low = mid
        return mid * self.freq  # 要转换回年化

    @property
    def YTC(self):
        if not self.callable:
            return None
        n = self.callYear * self.freq
        C = self.par * (self.coupon / self.freq)

        accuracy = 1e-4
        low = 0
        high = 0.5
        p_mid = 0
        while abs(self.price - p_mid) > accuracy:
            mid = (high + low) / 2
            p_high = C * PVCF(low, n) + self.callPrice * PVM(low, n)
            p_low = C * PVCF(high, n) + self.callPrice * PVM(high, n)
            p_mid = C * PVCF(mid, n) + self.callPrice * PVM(mid, n)
            if (self.price < p_high) and (self.price > p_mid):
                high = mid
            elif (self.price > p_low) and (self.price < p_mid):
                low = mid
        return mid * self.freq  # 要转换回年化

    def elapse(self, yearElapsed, inplace=False):
        '''
        Return a Bond Class, representing the same bond after given years.
        '''
        if yearElapsed > self.maturity:
            raise ValueError(
                "The year elapsed must not exceed the maturity of the bond.")
        maturity = self.maturity - yearElapsed

        callYear, callPrice = None, None
        putYear, putPrice = None, None
        if self.callable and self.callYear > yearElapsed:
            callYear = self.callYear - yearElapsed
            callPrice = self.callPrice
        if self.putable and self.putYear > yearElapsed:
            putYear = self.putYear - yearElapsed
            putPrice = self.putPrice
        if inplace:
            self.callYear = callYear
            self.callPrice = callPrice
            self.callable = not(callYear is None or callPrice is None)
            self.putYear = putYear
            self.putPrice = putPrice
            self.putable = not(putYear is None or putPrice is None)
            self.maturity = maturity
            return None
        else:
            return Bond(maturity, coupon=self.coupon, freq=self.freq, par=self.par,
                        YTM=self.YTM, price=self.price,
                        callPrice=callPrice, callYear=callYear,
                        putPrice=putPrice, putYear=putYear)
        # 为什么需要抽象类？
        # 因为有一个抽象类可以方便进行“同类继承”，否则就会需要重新设定很多参数

    def yeildDecompose(self, holdingYears=None, **arg):
        '''
        Decompose the Dollar Return into three parts.
        '''
        if holdingYears is None:
            holdingYears = self.maturity
        n = holdingYears * self.freq
        y = self.YTM / self.freq
        C = self.par * (self.coupon / self.freq)
        interest = n * C
        interestOnInterest = C * FVCF(y, n) - interest
        capitalGain = self.elapse(holdingYears).price - self.price
        
        return dict(interest=interest, 
                    interestOnInterest=interestOnInterest, 
                    capitalGain=capitalGain)


class Portfolio():
    '''
    一个债券的投资组合：
    可以用来查看是否有套利机会
    可以根据Yield Curve的变动来看收益的变动
    可以根据需求构造免疫策略
    BarBell, Bullet, Ladder, Rolling down

    需要继承bond的多数方法，比如也有duration，可以elapse等等
    '''
    def __init__(self):
        self.list = list()


def PVCF(rate, n):
    return sum(1/(1+rate)**t for t in range(1, n+1))


def FVCF(rate, n):
    return sum((1+rate)**t for t in range(1, n+1))


def PVM(rate, n):
    return 1/(1+rate)**n


def FVM(rate, n):
    return (1+rate)**n


if __name__ == '__main__':
    # bond = Bond(maturity=18, par=1000, price=1169, coupon=0.11, freq=2)
    bond = Bond(maturity=2, par=1000, YTM=0.09, coupon=0.1, freq=1)
    # bond = Bond(maturity=18, par=1000, price=1169, coupon=0.11, freq=2,
    #             putPrice=1000, putYear=5, callPrice=1055, callYear=8)
    bond.info
    # for i in range(1, 19):
    #     print(bond.elapse(i).price)
    # # bond.YTM += 0.0001
    # # bond.info
    # print(bond.yeildDecompose(3))
