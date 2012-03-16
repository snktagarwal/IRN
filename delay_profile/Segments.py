##

## Disambiguating stations

Delhi_stations = ['NDLS', 'DLI', 'DEC', 'DEE', 'DSA', 'NZM', 'ANVR', 'ANVT' ]
Kolkata_stations = [ 'HWH', 'SDAH', 'KOAA' ]
Mumbai_stations = [ 'CSTM', 'BCT', 'BDTS', 'DR', 'DDR', 'LTT' ]
Chennai_stations = [ 'MAS', 'MS', 'TBM' ]
Bangalore_stations = [ 'SBC', 'BNC', 'YPR', 'BNCE' ]
Hyderabad_stations = [ 'HYB', 'SC', 'KCG', 'BMT' ]

## This file lists all the imp segments, with in b/w stations 


###################  Northern Belt  #####################

# Amritsar(ASR) - Ambala(UMB) 
asr_umb = ['ASR','JRC','JUC','LDH','UMB']

#Ambala(UMB) - Panipat - Delhi
umb_delhi = ['UMB','PNP','DELHI']


# Ambala(UMB) - Moradabad(MB)
umb_mb = ['UMB','MB']

# Delhi- Jaipur(JP)
delhi_jp = ['DELHI','RE','AWR','JP']



################## Eastern & Gangetic Belt     #####################

# Delhi- mathura- Agra(AF/AGC)
delhi_agc = ['DELHI','MTJ','AGC']

# Delhi- aligarh- tundla - Etawah- Kanpur(CNB)
delhi_cnb= ['DELHI','ALJN','TDL','ETW','CNB']		# this gives better results than the following two individually
#delhi_tundla= ['DELHI','ALJN','TDL']
#tundla_cnb= ['TDL','ETW','CNB']


# Delhi- Moradabad(MB)
delhi_mb= ['DELHI','MB']

# Moradabad(MB)- Lucknow(LKO) 
mb_lko= ['MB','LKO']

# Kanpur(CNB)- Allahabad(ALD)
cnb_ald= ['CNB','ALD']


# Allahabad(ALD)- Mugalsarai(MGS)
ald_mgs= ['ALD','MGS']

# Kanpur(CNB) - Lucknow(LKO)
cnb_lko = ['CNB', 'LKO']

# Lucknow(LKO)- Varanasi(BSB)
lko_bsb = ['LKO','SLN','BSB']

#Varanasi(BSB)- Sonpur(SEE)
bsb_see= ['BSB','SEE']

# Mugalsarai(MGS)- Ara - Danapur - Patna(PNBE)
mgs_pnbe= ['MGS','ARA','PNBE']

# Sonpur(SEE)- Hajipur- Barauni- Katihar(KIR) 
see_kir= ['SEE','HJP','BJU','KIR']

#see_kir1= ['SEE','BJU'] 
#see_kir2 see-kir only 13, bju-kir: 42, hjp-kir: 17, see-hjp: 69, see-hjp-bju: 75,
#see_kir3 

# Mugalsarai(MGS)- Gaya(GAYA)
mgs_gaya= ['MGS','DOS','GAYA']

# Gaya(GAYA)- Gomoh - Dhanbad(DHN)
gaya_dhn= ['GAYA', 'GMO', 'DHN']

# Garwa Road - Barka Kana - Gomoh
garwa_gomoh = ['GHD', 'BRKA', 'GMO']

# Patna(PNBE)- Asansol(ASN)
pnbe_asn= ['PNBE','ASN']

# Dhanbad - Asansol(ASN)- Durgapur - Kolkata
dhanbad_kolkata= ['DHN', 'ASN','DGR','KOLKATA']

# Kolkata-Malda
kolkata_mldt= ['KOLKATA','MLDT']

# New Jalpaiguri - New Cooch Behar - New Bongaigon - Guwahati
njp_guwahati = ['NJP', 'NCB', 'NBQ', 'GHY']

################# Western Belt #######################

#Jaipur(JP)- Ajmer(AII)- Marwar(MJ)
jp_mj=['JP','AII','MJ']

#Marwar(MJ)- Abu Rd(ABR) - Ahmedabad(ADI)
mj_adi= ['MJ','ABR','ADI']

# Ahmedabad(ADI)- Anand(ANND) -Vadodara(BRC)- Surat (ST)
#adi_surat = ['ADI','ANND','BRC', 'ST'] 
adi_surat = ['ADI','BRC', 'ST'] 

# Ahmedabad(ADI) - Vadodara(BRC)
#adi_brc = ['ADI', 'BRC' ]

# Vadodara (BRC) - Surat (ST)
#brc_surat = ['BRC', 'ST']

# Bhusaval(BSL)- Manmad - Kalyan 
bsl_kalyan = ['BSL','MMR','KYN' ]

# Surat- Mumbai(CSTM/BCT)
st_mumbai = ['ST','MUMBAI']

# Mumbai-Pune(PUNE) 
mumbai_pune = ['MUMBAI','PUNE']

# KOTA(KOTA)- Ratlam(RTM)- Vadodara(BRC)
kota_brc= ['KOTA','RTM','BRC'] 

# Agra(AF/AGC)- KOTA(KOTA)



##################### South-eastern Belt ################
# Kolkata - Kharagpur(KGP)
kolkata_kgp = ['KOLKATA','KGP']

# Kharagpur(KGP)- Bhubaneswar(BBS)
kgp_bbs = ['KGP','BBS']

# Bhubaneswar(BBS)- Vizinagram - Vizag(VSKP) ::
bbs_vskp = ['BBS','VZM','VSKP']

# Vizag(VSKP) - Rajamundry - Vijaywada(BZA)
vskp_bza = ['VSKP', 'RJY', 'BZA']

# Vijaywada(BZA) - Guntur - Chennai(MAS/MS)
bza_chennai = ['BZA', 'GNT', 'CHENNAI'] 


##################### Central Belt #################

# Agra(AF/AGC)- Gwalior(GWL) - Jhansi(JHS) 
agc_jhs= ['AGC','GWL','JHS']

# Jhansi(JHS)- Bina - Bhopal(BPL) 
jhs_bpl= ['JHS','BINA','BPL']

# Bina - Katni(KTE) 
bina_kte= ['BINA','KTE']

# Ujjain-Bhopal(BPL)- Itarsi(ET) 
ujn_et= ['UJN', 'BPL', 'ET']

# Katni(KTE)- Jabalpur(JBP)- Itarsi(ET) 
kte_et= ['KTE','JBP','ET']

# Itarsi(ET)- Bhusaval(BSL) 
et_bsl= ['ET','BSL']


# Itarsi(ET)- Amla(AMLA) - Nagpur(NGP) 
et_ngp= ['ET','AMLA','NGP']

# Wardha - Kazipet - Secunderabad(SC) - Hyderabad(HYB) 
wardha_hydbad= ['WR', 'KZJ', 'HYDBAD']

# Katni(KTE)- Bilaspur(BSP) - Raipur(R) 
kte_r= ['KTE','BSP','R']

# Bilaspur - Rourkela
bilaspur_rourkela = [ 'BSP', 'ROU' ]

# Raipur(R) - Titlagarh - Vizianagram - Vishakhapatnam(VSKP) 
r_vskp= ['R', 'TIG', 'VZM', 'VSKP']

# Bhusaval(BSL)-Wardha-Nagpur(NGP)
bsl_ngp= ['BSL', 'WR', 'NGP']




##################### Southern Belt #################

# Pune(PUNE) - Solapur(SUR) -  Wadi(WADI) - Secunderabad/Hyderabad(HYB)
pune_hydbad = ['PUNE','SUR','WADI','HYDBAD']

# Wadi(WADI)- Guntakal(GTL) - Bangalore(SBC/BNC) 
wadi_blore = ['WADI','GTL','BLORE']

# Mumbai- RATNAGIRI(RN)-MADGAON(MAO) 
mumbai_mao= ['MUMBAI','RN','MAO']

# MADGAON(MAO)- MANGALORE(MAQ) 
mao_maq= ['MAO','MAQ']

# MANGALORE(MAQ)-Cannanore-Calicut(CLT)-Ernakulum(ERS)
maq_ers= ['MAQ', 'CAN', 'CLT','ERS']

# Ernakulum(ERS)-Alleppey-Trivandrum(TVC)
ers_tvc= ['ERS', 'ALLP', 'TVC']

# Guntakal(GTL) - Cuddapah(HX) - Renigunta(RU) - Chennai(MAS)
gtl_chennai = ['GTL','HX','RU','CHENNAI']

# Coimbatore - Salem - Chennai
coimbatore_chennai = [ 'CBE', 'SA', 'CHENNAI' ]


###############################################
# list containing all the above mentioned route segments

all_segments = [ asr_umb, umb_delhi, umb_mb, delhi_jp, delhi_agc, delhi_cnb, delhi_mb, mb_lko, cnb_ald, ald_mgs, cnb_lko, lko_bsb, bsb_see, mgs_pnbe, see_kir, mgs_gaya, gaya_dhn, garwa_gomoh, pnbe_asn, dhanbad_kolkata, kolkata_mldt, njp_guwahati, jp_mj, mj_adi, adi_surat, bsl_kalyan, st_mumbai, kota_brc, kolkata_kgp, kgp_bbs, bbs_vskp, vskp_bza, bza_chennai, agc_jhs, jhs_bpl, bina_kte, ujn_et, kte_et, et_bsl, et_ngp, wardha_hydbad, kte_r, bilaspur_rourkela, r_vskp, bsl_ngp, mumbai_pune, pune_hydbad, wadi_blore, mumbai_mao, mao_maq, maq_ers, ers_tvc, gtl_chennai, coimbatore_chennai ]


segments_with_max_traffic = [asr_umb, umb_delhi, delhi_cnb, delhi_agc, cnb_ald, ald_mgs, mgs_pnbe, see_kir, dhanbad_kolkata, adi_surat, bsl_kalyan, st_mumbai, kolkata_kgp, vskp_bza, agc_jhs, jhs_bpl, kte_et, et_bsl, wardha_hydbad, bza_chennai, lko_bsb, ujn_et ]


