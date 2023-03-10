
# from googletrans import Translator

# translator = Translator()

# with open('EnglishCountry.txt', 'r') as file:
#     # Read all the text from the file
#     text = file.read()
#     # Split the text into a list of strings (one string per line)
#     lines = text.split('\n')
#     print(lines)
#     thailist =[]
    # for i in lines:
    #     print(i)
    #     translation = translator.translate(str(i),dest="th",src="es",)
    #     if translation is not None:
    #         thailist.append(translation.text)
    #         print(translation.text)
    #     else:
    #         print('Translation failed for line:', i)
    #         thailist.append(translation.text)
    # print(thailist)
# for i in lines:
#     print(i)
#     try:
#         translation = translator.translate(str(i), dest="th", src="en")
#         thailist.append(translation.text)
#         print(translation.text)
#     except Exception as e:
#         print(f"Translation failed for line: {i}. Error: {e}")
#         thailist.append(None)
# print(thailist)
# englishlist = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Rep', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Congo {Democratic Rep}', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland {Republic}', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea North', 'Korea South', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar, {Burma}', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russian Federation', 'Rwanda', 'St Kitts & Nevis', 'St Lucia', 'Saint Vincent & the Grenadines', 'Samoa', 'San Marino', 'Sao Tome & Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad & Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
# thailist = ['อัฟกานิสถาน', 'แอลเบเนีย', 'แอลจีเรีย', 'อันดอร์รา', 'แองโกลา',
#  'แอนติกาและบาร์บูดา','อาร์เจนตินา', 'อาร์เมเนีย', 'ออสเตรเลีย', 'ออสเตรีย',
#   'อาเซอร์ไบจาน', 'บาฮามาส', 'บาห์เรน', 'บังกลาเทศ', 'บาร์เบโดส', 'เบลารุส', 'เบลเยียม',
#    'เบลีซ', 'เบนิน', 'ภูฏาน', 'โบลิเวีย', 'บอสเนียเฮอร์เซโกวีนา','บอตสวานา', 'บราซิล', 'บรูไน',
#     'บัลแกเรีย', 'บูร์กิน่า', 'บุรุนดี', 'กัมพูชา', 'แคเมอรูน', 'แคนาดา', 'กาบูเวร์ดี',
#      'แอฟริกากลาง', 'ชาด', 'ชิลี', 'จีน', 'โคลัมเบีย','โคมูรอส', 'คองโก',
#       'คองโก (ตัวแทนประชาธิปไตย)', 'คอสตาริกา', 'โครเอเชีย', 'คิวบา', 'ไซปรัส', 'สาธารณรัฐเช็ก', 'เดนมาร์ก',
#        'จิบูตี','โดมินิกา','สาธารณรัฐโดมินิกัน','ติมอร์ตะวันออก','เอกวาดอร์','อียิปต์','เอลซัลวาดอร์', 
#        'อิเควทอเรียลกินี', 'เอริเทรีย', 'เอสโตเนีย', 'เอธิโอเปีย', 'ฟิจิ', 'ฟินแลนด์', 'ฝรั่งเศส',
#         'กาบอง', 'แกมเบีย', 'จอร์เจีย', 'เยอรมนี', 'กานา', 'กรีซ', 'เกรนาดา',
#          'กัวเตมาลา', 'กินี', 'กินี-บิสเซา', 'กายอานา', 'เฮติ', 'ฮอนดูรัส', 'ฮังการี', 'ไอซ์แลนด์', 
#          'อินเดีย', 'อินโดนีเซีย', 'อิหร่าน', 'อิรัก', 'ไอร์แลนด์', 'อิสราเอล',
#           'อิตาลี', 'โกตดิวัวร์', 'จาไมกา', 'ญี่ปุ่น', 'จอร์แดน', 'คาซัคสถาน',
#            'เคนยา', 'คิริบาติ', 'เกาหลีเหนือ', 'เกาหลีใต้', 'โคโซโว', 'คูเวต', 'คีร์กีซสถาน',
#             'ลาว', 'ลัตเวีย', 'เลบานอน', 'เลโซโท', 'ไลบีเรีย', 'ลิเบีย', 'ลิกเตนสไตน์', 'ลิทัวเนีย', 'ลักเซมเบิร์ก',
#              'มาซิโดเนีย', 'มาดากัสการ์', 'มาลาวี', 'มาเลเซีย', 'มัลดีฟส์', 'มาลี', 'มอลตา',
#               'หมู่เกาะมาร์แชลล์', 'มอริเตเนีย', 'มอริเชียส', 'เม็กซิโก', 'ไมโครนีเซีย',
#                'มอลโดวา', 'โมนาโก', 'มองโกเลีย', 'มอนเตเนโกร', 'โมร็อกโก', 'โมซัมบิก', 
#                'พม่า','นามิเบีย', 'นาอูรู', 'เนปาล', 'เนเธอร์แลนด์', 'นิวซีแลนด์',
#                 'นิการากัว', 'ไนเจอร์', 'ไนจีเรีย', 'นอร์เวย์', 'โอมาน', 
#                 'ปากีสถาน', 'ปาเลา', 'ปานามา', 'ปาปัวนิวกินี', 'ปารากวัย', 'เปรู', 'ฟิลิปปินส์', 'โปแลนด์',
#                  'โปรตุเกส', 'กาตาร์', 'โรมาเนีย', 'รัสเซีย', 'รวันดา', 
#                  'เซนต์คิตส์และเนวิส', 'เซนต์ลูเซีย', 'เซนต์วินเซนต์และเกรนาดีนส์', 'ซามัว', 
#                  'ซานมาริโน', 'เซาตูเมและปรินซิปี', 'ซาอุดิอาราเบีย', 'เซเนกัล', 'เซอร์เบีย', 'เซเชลส์',
#                   'เซียร์ราลีโอน', 'สิงคโปร์', 'สโลวาเกีย', 'สโลวีเนีย', 'หมู่เกาะโซโลมอน', 'โซมาเลีย',
#                    'แอฟริกาใต้', 'ซูดานใต้', 'สเปน', 'ศรีลังกา', 'ซูดาน', 'ซูรินาเมะ',
#                     'สวาซิแลนด์', 'สวีเดน', 'สวิตเซอร์แลนด์', 'ซีเรีย', 'ไต้หวัน', 'ทาจิกิสถาน', 'แทนซาเนีย',
#                      'ประเทศไทย', 'ไป', 'ตองกา', 'ตรินิแดดและโตเบโก', 'ตูนิเซีย', 'ตุรกี',
#                       'เติร์กเมนิสถาน', 'ตูวาลู', 'ยูกันดา', 'ยูเครน', 'สหรัฐอาหรับเอมิเรตส์', 
#                       'อังกฤษ', 'สหรัฐ', 'อุรุกวัย', 'อุซเบกิสถาน', 'วานูอาตู', 'วาติกัน', 'เวเนซุเอลา', 
#                       'เวียดนาม', 'เยเมน', 'แซมเบีย', 'ซิมบับเว']
# dictofallcountrie= {}
# for i in range(len(englishlist)):
#     dictofallcountrie[thailist[i]] = englishlist[i]
# print(dictofallcountrie)







