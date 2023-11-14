import unittest
from flask import Flask, jsonify
from flask.testing import FlaskClient
from main import app



class AppTestCase(unittest.TestCase):

    username = 'VMG UNIT TEST TELEBOT'
    district = 'KONAK'
    neighborhood = 'ALSANCAK'
    StartDate = '01.01.2022'        # ("%d.%m.%Y")
    EndDate = '01.01.2023'
    MainTopic = 'SU / KANALİZASYON'
    SubTopic = 'BRANŞMAN (BİNA KOLU) ARIZALARI'
    Organisation = 'İZBB'
    Messages = 'UNIT TEST PROCESSİNG'
    Persons = {
            "ULAŞIM YATIRIMLARI-VEYSEL MURAT GÖRKEN": "5442107272",
            "KALİTE VE KURUMSAL GELİŞİM-AHMET KIPKIP": "5051284971",
            "BİLGİ İŞLEM-İBRAHİM GİLGİL": "5305807973",
            "ARGE-AHMET KIPKIP": "5435970114"
        }
    
    def setUp(self):
        self.app = app.test_client()

    def test_GetMainTopics(self):
        json = {"district": self.district, "neighborhood" : self.neighborhood}
        response = self.app.post('/Him/MainTopics', json=json)
    
        expected_response = [
            [
                "İZSU GENEL MÜDÜRLÜĞÜ",
                1961
            ],
            [
                "HEMŞEHRİ İLETİŞİM MERKEZİ",
                689
            ],
            [
                "KONAK BELEDİYE BAŞKANLIĞI",
                473
            ],
            [
                "ZABITA DAİRESİ BAŞKANLIĞI",
                247
            ],
            [
                "ZABITA DENETİM ŞUBE MÜDÜRLÜĞÜ",
                97
            ],
            [
                "ÇEVRE KORUMA VE KONTROL ŞUBE MÜDÜRLÜĞÜ",
                96
            ],
            [
                "İZBAN A.Ş",
                90
            ],
            [
                "ZABITA TRAFİK ŞUBE MÜDÜRLÜĞÜ",
                78
            ],
            [
                "TESİSLER BAKIM ONARIM ŞUBE MÜDÜRLÜĞÜ",
                78
            ],
            [
                "KENT TEMİZLİĞİ ŞUBE MÜDÜRLÜĞÜ",
                71
            ],
            [
                "ULAŞIM DAİRESİ BAŞKANLIĞI",
                59
            ],
            [
                "MERKEZ GÜNEY BÖLGESİ KANAL BAKIM ŞUBE MÜDÜRLÜĞÜ",
                58
            ],
            [
                "İZDENİZ A.Ş.",
                52
            ],
            [
                "FEN İŞLERİ DAİRESİ BAŞKANLIĞI",
                52
            ],
            [
                "SOSYAL YARDIMLAR ŞUBE MÜDÜRLÜĞÜ",
                48
            ],
            [
                "METRO A.Ş.",
                48
            ],
            [
                "İZELMAN A.Ş",
                44
            ],
            [
                "PARK VE BAHÇELER DAİRESİ BAŞKANLIĞI",
                41
            ],
            [
                "KÜLTÜR VE SANAT DAİRESİ BAŞKANLIĞI",
                40
            ],
            [
                "ÇEVRE KORUMA VE KONTROL DAİRESİ BAŞKANLIĞI",
                39
            ],
            [
                "DENİZ KORUMA ŞUBE MÜDÜRLÜĞÜ",
                39
            ],
            [
                "GÜNEY ALANLARI BAKIM ŞUBE MÜDÜRLÜĞÜ",
                37
            ],
            [
                "İKLİM DEĞİŞİKLİĞİ VE SIFIR ATIK DAİRESİ BAŞKANLIĞI",
                31
            ],
            [
                "MERKEZ BÖLGE TEKNİK AMİRLİĞİ",
                31
            ],
            [
                "KONAK ŞUBE MÜDÜRLÜĞÜ",
                28
            ],
            [
                "YAPI İŞLERİ DAİRESİ BAŞKANLIĞI",
                28
            ],
            [
                "YAPI İNCELEME VE İYİLEŞTİRME ŞUBE MÜDÜRLÜĞÜ",
                27
            ],
            [
                "ALTYAPI KOORDİNASYON ŞUBE MÜDÜRLÜĞÜ",
                27
            ],
            [
                "AĞAÇLANDIRMA ŞUBE MÜDÜRLÜĞÜ",
                26
            ],
            [
                "İZBETON A.Ş.",
                26
            ],
            [
                "ESHOT GENEL MÜDÜRLÜĞÜ",
                25
            ],
            [
                "KÜLTÜRPARK ŞUBE MÜDÜRLÜĞÜ",
                22
            ],
            [
                "SOSYAL MEDYA BİRİMİ",
                22
            ],
            [
                "ABONE İŞLERİ DAİRESİ BAŞKANLIĞI",
                22
            ],
            [
                "VETERİNER İŞLERİ ŞUBE MÜDÜRLÜĞÜ",
                21
            ],
            [
                "ULAŞIM PLANLAMA ŞUBE MÜDÜRLÜĞÜ",
                21
            ],
            [
                "FEN İŞLERİ ŞANTİYE ŞUBE MÜDÜRLÜĞÜ",
                21
            ],
            [
                "MERKEZ BÖLGE YOL İŞLERİ ŞUBE MÜDÜRLÜĞÜ",
                20
            ],
            [
                "İZFAŞ A.Ş",
                19
            ],
            [
                "SOSYAL HİZMETLER DAİRESİ BAŞKANLIĞI",
                18
            ],
            [
                "ULAŞIM PROJELERİ ŞUBE MÜDÜRLÜĞÜ",
                17
            ],
            [
                "GRAND PLAZA A.Ş.",
                17
            ],
            [
                "ULAŞIM KOORDİNASYON ŞUBE MÜDÜRLÜĞÜ",
                15
            ],
            [
                "KARŞIYAKA OTOBÜS İŞLETME ŞEFLİĞİ",
                14
            ],
            [
                "GENÇLİK VE SPOR ŞUBE MÜDÜRLÜĞÜ",
                13
            ],
            [
                "BORNOVA OTOBÜS İŞLETME ŞEFLİĞİ",
                13
            ],
            [
                "EŞREFPAŞA HASTANESİ EVDE BAKIM BİRİMİ",
                12
            ],
            [
                "TRAFİK HİZMETLERİ ŞUBE MÜDÜRLÜĞÜ",
                12
            ],
            [
                "AKILLI ÜCRET TOPLAMA SİSTEMİ MÜDÜRLÜĞÜ",
                11
            ],
            [
                "KENTSEL TASARIM VE KENT ESTETİĞİ ŞUBE MÜDÜRLÜĞÜ",
                9
            ],
            [
                "ETKİNLİK VE ORGANİZASYON ŞUBE MÜDÜRLÜĞÜ",
                9
            ],
            [
                "ALTYAPI ÇALIŞMALARI DENETİM VE İNCELEME ŞUBE MÜDÜRLÜĞÜ",
                9
            ],
            [
                "İMAR DENETİM- 2 ŞUBE MÜDÜRLÜĞÜ",
                8
            ],
            [
                "İZDOĞA A.Ş.",
                8
            ],
            [
                "KORUMA VE GÜVENLİK ŞUBE MÜDÜRLÜĞÜ",
                7
            ],
            [
                "İZMİR ULAŞIM MERKEZİ ŞUBE MÜDÜRLÜĞÜ",
                7
            ],
            [
                "KÜLTÜR VE SANAT ŞUBE MÜDÜRLÜĞÜ",
                6
            ],
            [
                "YAZILIM ŞUBE MÜDÜRLÜĞÜ",
                6
            ],
            [
                "İTFAİYE YANGIN VE ACİL MÜDAHALE ŞUBE MÜDÜRLÜĞÜ",
                6
            ],
            [
                "İZULAŞ A.Ş",
                5
            ],
            [
                "İDARİ İŞLER ŞUBE MÜDÜRLÜĞÜ",
                5
            ],
            [
                "DESTEK HİZMETLERİ DAİRESİ BAŞKANLIĞI",
                5
            ],
            [
                "BUCA OTOBÜS İŞLETME ŞEFLİĞİ",
                5
            ],
            [
                "TARİHSEL ÇEVRE VE KÜLTÜR VARLIKLARI ŞUBE MÜDÜRLÜĞÜ",
                5
            ],
            [
                "KENTSEL DÖNÜŞÜM ŞUBE MÜDÜRLÜĞÜ",
                5
            ],
            [
                "ÇEVRE VE İMAR ZABITASI ŞUBE MÜDÜRLÜĞÜ",
                5
            ],
            [
                "YAPI İŞLERİ ŞUBE MÜDÜRLÜĞÜ",
                4
            ],
            [
                "MÜHENDİSLİK JEOLOJİSİ ŞUBE MÜDÜRLÜĞÜ",
                4
            ],
            [
                "AŞEVLERİ ŞUBE MÜDÜRLÜĞÜ",
                4
            ],
            [
                "İNCİRALTI OTOBÜS İŞLETME ŞEFLİĞİ",
                4
            ],
            [
                "SU İSALE VE DAĞITIM DAİRESİ BAŞKANLIĞI",
                3
            ],
            [
                "KUZEY ALANLARI BAKIM ŞUBE MÜDÜRLÜĞÜ",
                3
            ],
            [
                "SOSYAL PROJELER DAİRESİ BAŞKANLIĞI",
                3
            ],
            [
                "ÇOCUK BELEDİYESİ ŞUBE MÜDÜRLÜĞÜ",
                3
            ],
            [
                "BASIN YAYIN VE HALKLA İLİŞKİLER DAİRESİ BAŞKANLIĞI",
                3
            ],
            [
                "İZMİR İNOVASYON VE TEKNOLOJİ A.Ş.",
                3
            ],
            [
                "KÜTÜPHANELER BİRİMİ",
                3
            ],
            [
                "KUZEY ATÖLYELER ŞUBE MÜDÜRLÜĞÜ",
                3
            ],
            [
                "GEDİZ OTOBÜS İŞLETME ŞUBE ŞEFLİĞİ",
                3
            ],
            [
                "TARIMSAL HİZMETLER DAİRESİ BAŞKANLIĞI",
                2
            ],
            [
                "KORUMA UYGULAMA VE DENETİM ŞUBE MÜDÜRLÜĞÜ",
                2
            ],
            [
                "DEPREM RİSK YÖNETİMİ VE KENTSEL İYİLEŞTİRME DAİRESİ BAŞKANLIĞI",
                2
            ],
            [
                "GENÇLİK VE SPOR HİZMETLERİ DAİRESİ BAŞKANLIĞI",
                2
            ],
            [
                "HARİTA DAİRESİ BAŞKANLIĞI",
                2
            ],
            [
                "ŞEHİR TİYATROLARI ŞUBE MÜDÜRLÜĞÜ",
                2
            ],
            [
                "TOPLU ULAŞIM HİZMETLERİ ŞUBE MÜDÜRLÜĞÜ",
                2
            ],
            [
                "DURAK VE HİZMET ALANLARI ŞUBE MÜDÜRLÜĞÜ",
                2
            ],
            [
                "REVİZYON YENİLEME PLANLARI ŞUBE MÜDÜRLÜĞÜ",
                2
            ],
            [
                "EMLAK YÖNETİMİ DAİRESİ BAŞKANLIĞI",
                2
            ],
            [
                "SOSYAL HİZMETLER ŞUBE MÜDÜRLÜĞÜ",
                2
            ],
            [
                "ADRES VE NUMARALAMA ŞUBE MÜDÜRLÜĞÜ",
                2
            ],
            [
                "MAKİNE İKMAL BAKIM VE ONARIM DAİRESİ BAŞKANLIĞI",
                2
            ],
            [
                "KANALİZASYON DAİRESİ BAŞKANLIĞI",
                2
            ],
            [
                "PROJELER DAİRESİ BAŞKANLIĞI",
                2
            ],
            [
                "PROJE TASARIM VE GELİŞTİRME ŞUBE MÜDÜRLÜĞÜ",
                2
            ],
            [
                "KENT ARŞİVİ, MÜZELER VE KÜTÜPHANELER ŞUBE MÜDÜRLÜĞÜ",
                2
            ],
            [
                "YEŞİL ALANLAR YAPIM ŞUBE MÜDÜRLÜĞÜ",
                2
            ],
            [
                "TARIMSAL EĞİTİM AR-GE VE KOORDİNASYON ŞUBE MÜDÜRLÜĞÜ",
                2
            ],
            [
                "YAPI KONTROL DAİRESİ BAŞKANLIĞI",
                1
            ],
            [
                "EŞREFPAŞA HASTANESİ BAŞHEKİMLİĞİ",
                1
            ],
            [
                "TARİHİ YAPILAR ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "BAKIM VE ONARIM ŞB.MÜDÜRLÜĞÜ",
                1
            ],
            [
                "MAKİNE İKMAL VE TESİSLER DAİRESİ BAŞKANLIĞI",
                1
            ],
            [
                "BAYRAKLI BELEDİYE BAŞKANLIĞI",
                1
            ],
            [
                "HALİHAZIR HARİTA VE APLİKASYON ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "UYGULAMA İMAR PLANLAMA ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "ENGELSİZMİR ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "KORUMA ALANLARI ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "BİLGİ İŞLEM DAİRESİ BAŞKANLIĞI",
                1
            ],
            [
                "YAZI İŞLERİ VE KARARLAR DAİRESİ BAŞKANLIĞI",
                1
            ],
            [
                "MUHTARLIKLAR VE YEREL HİZMETLER ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "SIFIR ATIK, PLANLAMA VE KATI ATIK DEĞERLENDİRME TESİSLERİ ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "YATIRIMLAR DENETİM ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "PARK VE BAHÇELER MÜDÜRLÜĞÜ",
                1
            ],
            [
                "PROTOKOL ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "TURİZM ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "ETÜD VE PROJELER DAİRESİ BAŞKANLIĞI",
                1
            ],
            [
                "BANLİYÖ SİSTEMLERİ ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "ŞİRKETLER VE KURULUŞLAR ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "KENT TARİHİ VE TANITIMI DAİRESİ BAŞKANLIĞI",
                1
            ],
            [
                "İMAR VE ŞEHİRCİLİK DAİRESİ BAŞKANLIĞI",
                1
            ],
            [
                "İZTARIM A.Ş",
                1
            ],
            [
                "İTFAİYE DAİRESİ BAŞKANLIĞI",
                1
            ],
            [
                "BASIN YAYIN VE TANITIM ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "TEKNİK İŞLER MÜDÜRLÜĞÜ",
                1
            ],
            [
                "BİLGİ AĞLARI VE SİSTEM YÖNETİMİ ŞUBE MÜDÜRLÜĞÜ",
                1
            ],
            [
                "ATIKSU TEKNİK VE İDARİ BİRİMİ",
                1
            ]
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_response)
        print(response.json)



if __name__ == '__main__':
    unittest.main()


