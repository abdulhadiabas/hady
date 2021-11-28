GENDER = (
    (1, 'مرد'),
    (2, 'زن'),
)
GENDER_MEN, GENDER_WOMAN = 1, 2

AGE = (
    (1, 'ژێر ١٠ ساڵ'),
    (2, '١٠-٢٠'),
    (3, '٢٠-٣٠'),
    (4, '٣٠-٤٠'),
    (5, '٤٠-٥٠'),
    (6, '٥٠-٦٠'),
    (7, 'زیاتر لە ٦٠ ساڵ')
)
AGE_UNDER_10, AGE_10_20, AGE_20_30, AGE_30_40, AGE_40_50, AGE_50_60, AGE_OVER_60 = 1, 2, 3, 4, 5, 6, 7

RECORD_STATES = (
    (1, 'پیش‌فرض'),
    (2, 'مورد تایید'),
)
RECORD_STATES_DEFAULT, RECORD_STATES_ACCEPTED = 1, 2


BASE_URL = 'https://tgdeep.herokuapp.com/'