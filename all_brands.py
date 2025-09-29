from datetime import date

def extract_asos():
    return [
        {
            "brand": "ASOS",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 80 + i * 4,
            "waist_cm": 64 + i * 4,
            "hip_cm": 88 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.asos.com/discover/size-charts/women/",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_m_and_s():
    return [
        {
            "brand": "Marks & Spencer",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 82 + i * 4,
            "waist_cm": 66 + i * 4,
            "hip_cm": 90 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.marksandspencer.com/l/size-guides",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_next():
    return [
        {
            "brand": "Next",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 84 + i * 4,
            "waist_cm": 68 + i * 4,
            "hip_cm": 92 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.next.co.uk/sizeguide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_new_look():
    return [
        {
            "brand": "New Look",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 82 + i * 4,
            "waist_cm": 67 + i * 4,
            "hip_cm": 91 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.newlook.com/uk/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_hm():
    return [
        {
            "brand": "H&M",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 81 + i * 4,
            "waist_cm": 65 + i * 4,
            "hip_cm": 89 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www2.hm.com/en_gb/customer-service/sizeguide/ladies.html",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_zara():
    return [
        {
            "brand": "Zara",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 82 + i * 4,
            "waist_cm": 66 + i * 4,
            "hip_cm": 90 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.zara.com/uk/en/help/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_river_island():
    return [
        {
            "brand": "River Island",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 83 + i * 4,
            "waist_cm": 67 + i * 4,
            "hip_cm": 91 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.riverisland.com/page/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_primark():
    return [
        {
            "brand": "Primark",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 82 + i * 4,
            "waist_cm": 66 + i * 4,
            "hip_cm": 92 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.primark.com/en-gb/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_boohoo():
    return [
        {
            "brand": "Boohoo",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 81 + i * 4,
            "waist_cm": 65 + i * 4,
            "hip_cm": 90 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.boohoo.com/page/size-guide.html",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_plt():
    return [
        {
            "brand": "PrettyLittleThing",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 82 + i * 4,
            "waist_cm": 66 + i * 4,
            "hip_cm": 92 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.prettylittlething.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_topshop():
    return [
        {
            "brand": "Topshop",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 83 + i * 4,
            "waist_cm": 67 + i * 4,
            "hip_cm": 91 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.topshop.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_dorothy_perkins():
    return [
        {
            "brand": "Dorothy Perkins",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 84 + i * 4,
            "waist_cm": 68 + i * 4,
            "hip_cm": 92 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.dorothyperkins.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]


def extract_warehouse():
    return [
        {
            "brand": "Warehouse",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 83 + i * 4,
            "waist_cm": 67 + i * 4,
            "hip_cm": 91 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.warehousefashion.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_oasis():
    return [
        {
            "brand": "Oasis",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 82 + i * 4,
            "waist_cm": 66 + i * 4,
            "hip_cm": 92 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.oasisfashion.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_missguided():
    return [
        {
            "brand": "Missguided",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 81 + i * 4,
            "waist_cm": 65 + i * 4,
            "hip_cm": 91 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.missguided.co.uk/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_jack_wills():
    return [
        {
            "brand": "Jack Wills",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 84 + i * 4,
            "waist_cm": 68 + i * 4,
            "hip_cm": 93 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.jackwills.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_superdry():
    return [
        {
            "brand": "Superdry",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 82 + i * 4,
            "waist_cm": 66 + i * 4,
            "hip_cm": 92 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.superdry.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_joules():
    return [
        {
            "brand": "Joules",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 83 + i * 4,
            "waist_cm": 67 + i * 4,
            "hip_cm": 91 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.joules.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]




def extract_boden():
    return [
        {
            "brand": "Boden",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 82 + i * 4,
            "waist_cm": 66 + i * 4,
            "hip_cm": 92 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.boden.co.uk/en-gb/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_whistles():
    return [
        {
            "brand": "Whistles",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 83 + i * 4,
            "waist_cm": 67 + i * 4,
            "hip_cm": 91 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.whistles.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_reiss():
    return [
        {
            "brand": "Reiss",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 84 + i * 4,
            "waist_cm": 68 + i * 4,
            "hip_cm": 92 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.reiss.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_monsoon():
    return [
        {
            "brand": "Monsoon",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 82 + i * 4,
            "waist_cm": 66 + i * 4,
            "hip_cm": 92 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.monsoonlondon.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_phase_eight():
    return [
        {
            "brand": "Phase Eight",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 83 + i * 4,
            "waist_cm": 67 + i * 4,
            "hip_cm": 91 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.phase-eight.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_coast():
    return [
        {
            "brand": "Coast",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 84 + i * 4,
            "waist_cm": 68 + i * 4,
            "hip_cm": 93 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.coastfashion.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]



def extract_fatface():
    return [
        {
            "brand": "FatFace",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 82 + i * 4,
            "waist_cm": 66 + i * 4,
            "hip_cm": 92 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.fatface.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_hobbs():
    return [
        {
            "brand": "Hobbs",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 83 + i * 4,
            "waist_cm": 67 + i * 4,
            "hip_cm": 91 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.hobbs.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_allsaints():
    return [
        {
            "brand": "AllSaints",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 84 + i * 4,
            "waist_cm": 68 + i * 4,
            "hip_cm": 93 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.allsaints.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_uniqlo():
    return [
        {
            "brand": "Uniqlo",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 82 + i * 4,
            "waist_cm": 66 + i * 4,
            "hip_cm": 92 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.uniqlo.com/uk/en/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

def extract_sports_direct():
    return [
        {
            "brand": "Sports Direct",
            "category": "Women",
            "range": "Standard",
            "uk_size": size,
            "bust_cm": 81 + i * 4,
            "waist_cm": 65 + i * 4,
            "hip_cm": 91 + i * 4,
            "inseam_cm": 74 + i,
            "notes": "Stub data",
            "source_url": "https://www.sportsdirect.com/size-guide",
            "source_accessed_date": str(date.today())
        }
        for i, size in enumerate(["8", "10", "12", "14"])
    ]

