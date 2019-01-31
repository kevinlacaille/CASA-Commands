#Band7 = C+
#z = 5.656
#line at 285.53739 GHz
#SPT0348 in field 4
#C+ in spw 1
#data between channels 9-118, to cut them out in clean write start=9, nchan=int(118-9)
#line between channels 9~80




delmod('../../uid___A002_Xbbcb1f_X5ffd.ms.split.cal')
#dirty line

tclean(vis='../../uid___A002_Xbbcb1f_X5ffd.ms.split.cal', imagename='line/spt0348_CII_dirty_briggs', field='4', spw='1', niter=0, interactive=False, specmode='cube', restfreq='285.53739 GHz', cell='0.061 arcsec', imsize=720, weighting='briggs', robust=float(0.5))

#uvcontsub

uvcontsub(vis='../../uid___A002_Xbbcb1f_X5ffd.ms.split.cal/', field='4', spw='1', fitspw='1:80~118', fitorder=0, excludechans=False, want_cont=False)

#dirty contsub line

tclean(vis='../../uid___A002_Xbbcb1f_X5ffd.ms.split.cal.contsub/', imagename='line/spt0348_CII_dirty_contsub_briggs', niter=0, interactive=False, specmode='cube', restfreq='285.53739 GHz', cell='0.061 arcsec', imsize=720, weighting='briggs', robust=float(0.5))

#dirty continuum

tclean(vis='../../uid___A002_Xbbcb1f_X5ffd.ms.split.cal/', imagename='continuum/spt0348_b7ctm_dirty_briggs', field='4', spw='0,1:80~119,2,3', niter=0, interactive=False, specmode='mfs', cell='0.061 arcsec', imsize=720, weighting='briggs', robust=float(0.5))

#clean continuum to 2sigma
tclean(vis='../../uid___A002_Xbbcb1f_X5ffd.ms.split.cal/', imagename='continuum/spt0348_b7ctm_clean2sig_briggs', field='4', spw='0,1:80~119,2,3', niter=1000, interactive=True, threshold=str(float(2*0.30))+'mJy', specmode='mfs', cell='0.061 arcsec', imsize=720, weighting='briggs', robust=float(0.5))

#clean line to 2sigma
tclean(vis='../../uid___A002_Xbbcb1f_X5ffd.ms.split.cal.contsub/', imagename='line/spt0348_CII_clean2sig_contsub_briggs', niter=1000, interactive=True, threshold=str(float(2*0.75))+'mJy', specmode='cube', restfreq='285.53739 GHz', cell='0.061 arcsec', imsize=720, weighting='briggs', robust=float(0.5))


#moment-0 maps: integrated fields 
immoments(imagename='line/spt0348_CII_clean2sig_contsub_briggs.image', moments=[0], outfile='moment_maps/spt0348_CII_clean2sig_contsub_briggs_W.mom0', chans='9~80', includepix=[2*0.75*1e-3, 1000])
immoments(imagename='line/spt0348_CII_clean2sig_contsub_briggs.image', moments=[0], outfile='moment_maps/spt0348_CII_clean2sig_contsub_briggs_E.mom0', chans='9~80', includepix=[2*0.75*1e-3, 1000])

# pb-cor cube
impbcor(imagename='line/spt0348_CII_clean2sig_contsub_briggs.image/', pbimage='line/spt0348_CII_clean2sig_contsub_briggs.pb', outfile='line/spt0348_CII_clean2sig_contsub_briggs_pcbor')
impbcor(imagename='continuum/spt0348_b7ctm_clean2sig_briggs.image', pbimage='continuum/spt0348_b7ctm_clean2sig_briggs.pb', outfile='continuum/spt0348_b7ctm_clean2sig_briggs_pbcor')
# make pb image from cube for moment map pb-cor
imsubimage(imagename='line/spt0348_CII_clean2sig_contsub_briggs.pb', chans='60', outfile='line/spt0348_CII_clean2sig_contsub_briggs_pb_centrecan')
# pb cor moment-0 map
impbcor(imagename='moment_maps/spt0348_CII_clean2sig_contsub_briggs_W.mom0', pbimage='line/spt0348_CII_clean2sig_contsub_briggs_pb_centrecan', outfile='moment_maps/spt0348_CII_clean2sig_contsub_briggs_W.mom0_pbcor')
impbcor(imagename='moment_maps/spt0348_CII_clean2sig_contsub_briggs_E.mom0', pbimage='line/spt0348_CII_clean2sig_contsub_briggs_pb_centrecan', outfile='moment_maps/spt0348_CII_clean2sig_contsub_briggs_E.mom0_pbcor')




