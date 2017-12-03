# -*- coding: utf-8 -*-

class GuiDraw:
    P_PATTERN = '<p>%s</p>'
    RED_PATTERN = '<span style=\" font-size:12pt; font-weight:400; color:#FF0c32;\" > %s </span>'
    GREEN_PATTERN = '<span style=\" font-size:12pt; font-weight:400; color:#5A9755;\" > %s </span>'
    BLUE_PATTERN = '<span style=\" font-size:12pt; font-weight:400; color:#4280A8;\" > %s </span>'
    PEP_PATTERN = '<span style=\" font-size:12pt; font-weight:400; color:#945165;\" > %s </span>'
    BROWN_PATTERN = '<span style=\" font-size:12pt; font-weight:400; color:#cc692e;\" > %s </span>'
    WHITE_PATTERN = '<span style=\" font-size:12pt; font-weight:400; color:#c9f9ff;\" > %s </span>'
    SPACE_PATTERN = '&nbsp;&nbsp;&nbsp;&nbsp;'
    P_W_PATTERN = '<p><span style=\" font-size:12pt; font-weight:400; color:#FF0c32;\" > %s </span></p>'
    html = ''

    def draw_text(self, word, conf):
        # Word
        self.html += self.P_PATTERN % (self.RED_PATTERN % word['word'])
        # pronunciation
        if word['pronunciation']:
            uncommit = ''
            if '英' in word['pronunciation']:
                uncommit += self.WHITE_PATTERN % u'英 ' + self.PEP_PATTERN % word['pronunciation']['英'] + self.SPACE_PATTERN
            if '美' in word['pronunciation']:
                uncommit += self.WHITE_PATTERN % u'美 ' + self.PEP_PATTERN % word['pronunciation']['美']
            if '' in word['pronunciation']:
                uncommit = self.WHITE_PATTERN % u'英/美 ' + self.PEP_PATTERN % word['pronunciation']['']
            self.html += self.P_PATTERN % uncommit
        # paraphrase
        for v in word['paraphrase']:
            self.html += self.P_PATTERN % (self.BLUE_PATTERN % v)
        # short desc
        if word['rank']:
            self.html += self.P_PATTERN % (self.RED_PATTERN % word['rank'])
        if word['pattern']:
            self.html += self.P_PATTERN % (self.RED_PATTERN % word['pattern'].strip())
        # sentence
        if conf:
            count = 1
            if word['sentence']:
                self.html += self.P_PATTERN % ''
                if len(word['sentence'][0]) == 2:
                    collins_flag = False
                else:
                    collins_flag = True
            else:
                return
            for v in word['sentence']:
                if collins_flag:
                    # collins dict
                    if len(v) != 3:
                        continue
                    if v[1] == '' or len(v[2]) == 0:
                        continue
                    self.html += '<p>'
                    if v[1].startswith('['):
                        self.html += (self.WHITE_PATTERN % (str(count) + '.&nbsp;')
                                      + self.GREEN_PATTERN % (v[1]))
                    else:
                        self.html += (self.WHITE_PATTERN % (str(count) + '.&nbsp;')
                                      + self.GREEN_PATTERN % ('[' + v[1] + ']'))
                    self.html += self.WHITE_PATTERN % v[0] + '</p>'
                    for sv in v[2]:
                        self.html += self.P_PATTERN % (self.GREEN_PATTERN % u'&nbsp;&nbsp;例: ' +
                                                       self.BROWN_PATTERN % (sv[0] + sv[1]))
                    count += 1
                    self.html += self.P_PATTERN % ''
                else:
                    # 21 new year dict
                    if len(v) != 2:
                        continue
                    self.html += '<p>' + (self.WHITE_PATTERN % (str(count) + '.&nbsp;')
                                          + self.GREEN_PATTERN % '[例]')
                    self.html += self.WHITE_PATTERN % v[0] + '</p>'
                    self.html += self.P_PATTERN % (self.BROWN_PATTERN % v[1])
                    count += 1

    def draw_zh_text(self, word, conf):
        # Word
        self.html += self.P_PATTERN % (self.RED_PATTERN % word['word'])
        # pronunciation
        if word['pronunciation']:
            self.html += self.P_PATTERN % (self.PEP_PATTERN % word['pronunciation'])
        # paraphrase
        if word['paraphrase']:
            for v in word['paraphrase']:
                v = v.replace('  ;  ', ',&nbsp;')
                self.html += self.P_PATTERN % (self.BLUE_PATTERN % v)
        # complex
        if conf:
            # description
            count = 1
            if word["desc"]:
                self.html += self.P_PATTERN % ''
                for v in word['desc']:
                    if not v:
                        continue
                    # sub title
                    self.html += '<p>' + self.WHITE_PATTERN % (str(count) + '.&nbsp;')
                    v[0] = v[0].replace(';', ',')
                    self.html += self.GREEN_PATTERN % v[0] + '</p>'
                    # sub example
                    sub_count = 0
                    if len(v) == 2:
                        for e in v[1]:
                            if sub_count % 2 == 0:
                                e = e.strip().replace(';', '')
                                self.html += '<p>' + self.BROWN_PATTERN % (self.SPACE_PATTERN + e + self.SPACE_PATTERN)
                            else:
                                self.html += self.WHITE_PATTERN % e + '</p>'
                            sub_count += 1
                    count += 1
            # example
            if word['sentence']:
                count = 1
                self.html += self.P_PATTERN % (self.RED_PATTERN % '例句:')
                self.html += self.P_PATTERN % ''
                for v in word['sentence']:
                    if len(v) == 2:
                        self.html += self.P_PATTERN % ''
                        self.html += self.P_PATTERN % (self.WHITE_PATTERN % (str(count) + '.&nbsp;')
                                                       + self.BROWN_PATTERN % v[0] + self.SPACE_PATTERN
                                                       + self.WHITE_PATTERN % v[1])
                    count += 1

