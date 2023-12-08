import zfit

from rkex_model import model

from logzero    import logger  as log
from builder    import builder as cb_builder

#---------------------------------------------------------------
class rk_model(model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._d_val = {} 
        self._d_var = {} 
    #---------------------------------------------------------------
    def _get_dset_trig(self, preffix):
        [chan, dset, kind, _ ] = preffix.split('_')
    
        if   chan == 'mm':
            trig = 'MTOS'
        elif chan == 'ee' and kind == 'TOS': 
            trig = 'ETOS'
        elif chan == 'ee' and kind == 'TIS': 
            trig = 'GTIS'
        else:
            log.error(f'Invalid channel: {chan}')
            raise ValueError
    
        return dset, trig
    #---------------------------------------------------------------
    def _is_good_constraint(self, name):
        '''
        TIS muon is not used (PDF dropped in base class), no need for constraints for these
        parameters
        '''
        if '_mm_' in name and '_TIS_' in name:
            return False

        return True
    #---------------------------------------------------------------
    def _add_constraints(self, d_cns):
        d_val = { name : cns[0]    for name, cns in d_cns.items() if self._is_good_constraint(name)}
        d_var = { name : cns[1]**2 for name, cns in d_cns.items() if self._is_good_constraint(name)}

        self._d_val.update(d_val)
        self._d_var.update(d_var)
    #---------------------------------------------------------------
    def _get_combinatorial(self, preffix, nent):
        dset, trig    = self._get_dset_trig(preffix) 
        obj           = cb_builder(dset=dset, trigger=trig, vers='v5', q2bin='high', const=False)
        obj.cache_path= './cb_buider.tar.gz'
        cmb, d_cns    = obj.get_pdf(obs=self._obs, preffix=f'cb_{preffix}') 

        self._add_constraints(d_cns)

        ncb           = zfit.Parameter(f'ncb_{preffix}', 10 * nent, 0, 100000)
        cbkg          = cmb.create_extended(ncb)

        return cbkg
    #---------------------------------------------------------------
    def _get_signal(self, preffix, mu=None, sg=None, nent=None):
        mu, sg = self._get_peak_pars(preffix, mu=mu, sg=sg)

        gauss  = zfit.pdf.Gauss(obs=self._obs, mu=mu, sigma=sg)
        nsg    = zfit.Parameter(f'nsg_{preffix}', nent, 0, 100000)
        esig   = gauss.create_extended(nsg)

        return esig
    #---------------------------------------------------------------
    def _get_pdf(self, preffix='', mu=None, sg=None, nent=None):
        preffix= f'{preffix}_{self._preffix}'

        cbkg   = self._get_combinatorial(preffix, nent)
        esig   = self._get_signal(preffix, mu=mu, sg=sg, nent=nent)
        pdf    = zfit.pdf.SumPDF([esig, cbkg]) 

        return pdf 
    #---------------------------------------------------------------
    def get_cons(self):
        '''
        Will return constraints on model parameters 

        Returns
        -----------
        d_val, d_var: Tuple of dictionaries pairing parameter name with value (mu of Gaussian) and 
        variance respectively.
        '''
        self._initialize()

        log.debug('-' * 20)
        log.debug(f'{"Name":<40}{"Value":<15}{"Variance":<15}')
        log.debug('-' * 20)
        for name in self._d_val:
            val = self._d_val[name]
            var = self._d_var[name]

            log.debug(f'{name:<40}{val:<15.3f}{var:<15.3f}')
        log.debug('-' * 20)

        return self._d_val, self._d_var
#---------------------------------------------------------------

