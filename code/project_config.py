import sys
sys.path.append('utils')

TR = 2.5
#we choose cutoff value values by inspecting the histogram of data values of the standard mni brain
MNI_CUTOFF = 5000

MIN_STD_SHAPE = (91, 109, 91)

groups = {"fmri_con":("011", "012", "015", "020", "023", "035", "036", "037"),
          "fmri_con_sib":("010", "013", "014", "016", "021", "022", "038"),
          "fmri_scz":("001", "005", "007", "009", "017", "027", "031"),
          "fmri_scz_sib":("002", "003", "004", "006", "008", "018", "019", "024", "025", "026", "028", "029", "030", "032", "033", "034", "039", "040", "041")}

