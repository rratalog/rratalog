import toml, glob, jinja2
import pandas as pd
from pprint import pprint as print
from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import argparse

make_html = True #if True, will save rratalog.html
make_csv = True #if True, will save rratalog.csv
make_tex = False #if True, will save rratalog.tex

##########
#Define functions
##########

def error_string_dec(value,err):
    zeroflag=0

    if type(err)==str:
        err = float(err)
    power_err = np.log10(err)
    n_sigfigs = np.floor(power_err)

    if type(value)==str:
        #If the number in the n_sigfigs place after the zero is a decimal, add a zero
        if value.split('.')[-1][-1*int(n_sigfigs)-1]=='0' and not len(value.split('.')[-1])==1:
            zeroflag = 1
        else:
            zeroflag=0
        value = float(value)

    if err > 1:
        n_err = err
        err_string = str(np.round(value,int(-1*n_sigfigs)+1)) + '(' + str(n_err) + ')'
    else:
        n_err = int(np.round(err / (10 ** np.floor(power_err)),0))
        err_string = str(np.round(value,int(-1*n_sigfigs)))
        if zeroflag==1:
            err_string += '0'
        err_string += '(' + str(n_err) + ')'


    if len(str(float(err)).partition('.')[0]) > 1 and not 'e' in str(float(err)).partition('.')[0]: #if error is > 10
        n_err = err
        err_string = str(value) + '(' + str(n_err) + ')'

    return err_string

def error_string_coords(coord,err):

    if "00:00:" in err:
        #error is on the order of arcsecs, use error_string_dec
        c_zeroflag = 1
        new_value = coord.split(':')[-1]
        new_error = err.split(':')[-1]
        beginval = coord.split(':')[0] + ':' + coord.split(':')[1]
        if '.' in new_error:
            end_new_error = new_error.split('.')[-1]
            if int(end_new_error) >= 10:
                #truncate leading zeroes of new_new_error
                end_new_error=end_new_error.lstrip('0')
                endstring = new_value + '(' + end_new_error + ')'
                c_zeroflag = 0
            else:
                endstring = error_string_dec(new_value,new_error)
        else:
            endstring = error_string_dec(int(new_value),int(new_error))

        errstring = beginval + ':'
        if new_value.startswith('0') and c_zeroflag==1:
            errstring += '0'
        errstring += endstring

    elif '00:' in err and ':' in coord:
        if len(err.split(':')) >= 3:
            #error is on the order of arcsecs
            beginval = coord.split(':')[0] + ':' + coord.split(':')[1] + ':' + coord.split(':')[2]
            errstr = err.partition(':')[-1]
            errstring = beginval + '(' + errstr + ')'
        else:
            #error is on the order of arcmins
            errstr = err.partition(':')[-1]
            if errstr.startswith('0'):
                beginval = coord.split(':')[0]
                endstring = error_string_dec(int(coord.split(':')[1]),int(errstr))
                if coord.split(':')[1].startswith('0'):
                    errstring = beginval + ':0' + endstring
                else:
                    errstring = beginval + ':' + endstring
            else:
                beginval = coord.split(':')[0] + ':' + coord.split(':')[1]
                errstring = beginval + '(' + errstr + ')'
    else:
        errstring=coord

    return errstring

##########
#Make rratalog
##########

table_keys = ["Name","RA", "Dec", "DM", "Period", "Pdot", "Pepoch", "Frequency", "Fdot", "Bsurf", "Edot", "Tau", "l", "b", "BurstRate", "Flux", "Width"]
units = ["","hh:mm:ss.ss","dd:mm:ss.ss","pc cm^-3", "s", "10^-15 s/s", "", "Hz", "10^-15 Hz/s", "10^12 G", "10^31 erg/s", "Myr", "deg", "deg","hr^-1","mJy","ms"]
df_keys = table_keys + [x+"_ref" for x in table_keys]

unit_keys=[]
for i in range(len(table_keys)):
    if len(units[i]) > 0:
        unit_keys.append(table_keys[i] + '   (' + units[i] + ')')
    else:
        unit_keys.append(table_keys[i])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate RRATalog outputs")
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()
    verbose = args.verbose

    def vprint(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)

    list_of_rrats = glob.glob("J*.toml")
    list_of_rrats.sort()
    display_dict = {}
    rrat_dict = {}

    for key in df_keys:
        display_dict[key] = []
        rrat_dict[key] = []


    full_display_df = pd.DataFrame(rrat_dict)
    #print(full_display_df.columns)

    for rrat in list_of_rrats:
        display_dict={}
        for key in table_keys:
            display_dict[key] = []
            display_dict[key+"_ref"] = []
        try:
            rrat_toml = toml.load(rrat)

            #Calculate positions, period/frequency, and derivatives up here so we don't have to do it in the for loop
            try:
                p0 = rrat_toml["Period"]["value"]
                p0_error = rrat_toml["Period"]["error"]
                f0 = 1./p0
                f0_error = p0_error/(p0**2.)
            except KeyError:
                pass

            try:
                p1 = rrat_toml["Pdot"]["value"]
                p1_error = rrat_toml["Pdot"]["error"]
                f1 = (-1.*p1)/(p0**2)
                f1_error = abs((p1_error*f1)/(p1))
            except KeyError:
                pass

            pos = rrat_toml["RA"]["value"] + " " + rrat_toml["Dec"]["value"]
            c = SkyCoord(pos, unit=(u.hourangle, u.deg))
            c_gal = c.galactic

            for key in table_keys:

                if key =="Name":
                    if "value" in rrat_toml[key]:
                        display_dict[key].append(rrat_toml[key]["value"])
                        if "ref" in rrat_toml[key]:
                            display_dict[key+"_ref"].append(rrat_toml[key]["ref"])
                        else:
                            display_dict[key + "_ref"].append('--')
                    else:
                        pass

                elif key=="RA" or key=="Dec":
                    try:
                        z = rrat_toml[key]
                        if rrat_toml[key]["error"] == False:
                            display_dict[key].append(rrat_toml[key]["value"])
                            display_dict[key+"_ref"].append(rrat_toml[key]["ref"])
                        else:
                            err_string = error_string_coords(rrat_toml[key]["value"],rrat_toml[key]["error"])
                            display_dict[key].append(err_string)
                            display_dict[key+"_ref"].append(rrat_toml[key]["ref"])
                    except KeyError:
                        display_dict[key].append('--')
                        display_dict[key+"_ref"].append('--')


                elif key=="DM":
                    try:
                        z = rrat_toml[key]
                        if rrat_toml[key]["error"] == False:
                            display_dict[key].append(rrat_toml[key]["value"])
                            display_dict[key+"_ref"].append(rrat_toml[key]["ref"])
                        else:
                            err_string = error_string_dec(rrat_toml[key]["value"],rrat_toml[key]["error"])
                            display_dict[key].append(err_string)
                            display_dict[key+"_ref"].append(rrat_toml[key]["ref"])
                    except KeyError:
                        display_dict[key].append('--')
                        display_dict[key+"_ref"].append('--')

                elif key=="Period":
                    try:
                        z = rrat_toml[key]
                        if rrat_toml[key]["error"] == False:
                            display_dict[key].append(p0)
                            display_dict[key+"_ref"].append(rrat_toml[key]["ref"])
                        else:
                            err_string = error_string_dec(p0,p0_error)
                            display_dict[key].append(err_string)
                            display_dict[key+"_ref"].append(rrat_toml[key]["ref"])
                    except KeyError:
                        display_dict[key].append('--')
                        display_dict[key+"_ref"].append('--')

                elif key=="Pdot":
                    try:
                       z = rrat_toml[key]
                       if rrat_toml[key]["error"] == False:
                           display_dict[key].append(p1*1e15)
                           display_dict[key+"_ref"].append(rrat_toml["Pdot"]["ref"])
                           vprint(rrat_toml["Name"]["value"])
                       else:
                            if len(str(p1).partition('.')[2]) > 10:
                                p1round = np.round(p1,10)
                                #multiplying by 1e15 introduces weird rounding errors; this truncates them
                                err_string = error_string_dec(p1round*1e15,p1_error*1e15)
                            else:
                                err_string = error_string_dec(p1*1e15,p1_error*1e15)
                            display_dict[key].append(err_string)
                            display_dict[key+"_ref"].append(rrat_toml[key]["ref"])
                    except KeyError:
                        display_dict[key].append('--')
                        display_dict[key+"_ref"].append('--')

                elif key=="Pepoch":
                    try:
                        z = rrat_toml[key]
                        display_dict[key].append(z["value"])
                        display_dict[key+"_ref"].append(rrat_toml[key]["ref"])
                    except KeyError:
                        display_dict[key].append('--')
                        display_dict[key+"_ref"].append('--')

                elif key=="Frequency":
                    try:
                        z = rrat_toml["Period"]
                        if rrat_toml["Period"]["error"] == False:
                            #If there's no period error, there's no frequency error
                            #Truncate the frequency at the same place the period is truncated at
                            n_sigfigs = len(str(p0).partition('.')[-1])
                            f0 = np.round(f0,n_sigfigs)
                            display_dict[key].append(f0)
                            display_dict[key+"_ref"].append(rrat_toml["Period"]["ref"])
                        else:
                            err_string = error_string_dec(f0,f0_error)
                            display_dict[key].append(err_string)
                            display_dict[key+"_ref"].append(rrat_toml["Period"]["ref"])
                    except KeyError:
                        display_dict[key].append('--')
                        display_dict[key+"_ref"].append('--')

                elif key=="Fdot":
                    try:
                        z = rrat_toml["Pdot"]
                        if rrat_toml["Pdot"]["error"] == False:
                            display_dict[key].append(f1*1e15)
                            display_dict[key+"_ref"].append(rrat_toml["Pdot"]["ref"])
                        else:
                            if len(str(f1).partition('.')[2]) > 10:
                                f1round = np.round(f1*1e15,10)
                                err_string = error_string_dec(f1round,f1_error*1e15)
                            else:
                                err_string = error_string_dec(f1*1e15,f1_error*1e15)
                            display_dict[key].append(err_string)
                            display_dict[key+"_ref"].append(rrat_toml["Pdot"]["ref"])
                    except KeyError:
                        display_dict[key].append('--')
                        display_dict[key+"_ref"].append('--')

                #Timing derived parameters from P/Pdot

                elif key=="Tau":
                    try:
                        z = rrat_toml["Pdot"]
                        tau = p0/(2*p1)*(3.171e-14)
                        display_dict[key].append(np.round(tau,1))
                        display_dict[key+"_ref"].append(rrat_toml["Pdot"]["ref"])
                        #error probably not relevant- much larger than calculated
                    except KeyError:
                        display_dict[key].append('--')
                        display_dict[key+"_ref"].append('--')


                elif key=="Bsurf":
                    try:
                        z= rrat_toml["Pdot"]
                        bsurf = (3.2e19)*( (p0*p1)**0.5 )*(1e-12)
                        display_dict[key].append(np.round(bsurf,1))
                        display_dict[key+"_ref"].append(rrat_toml["Pdot"]["ref"])
                    except KeyError:
                        display_dict[key].append('--')
                        display_dict[key+"_ref"].append('--')


                elif key=="Edot":
                    try:
                        z= rrat_toml["Pdot"]
                        edot = (3.95)*(p1/1e-15)*( (1/p0)**3 )
                        display_dict[key].append(np.round(edot,1))
                        display_dict[key+"_ref"].append(rrat_toml["Pdot"]["ref"])
                    except KeyError:
                        display_dict[key].append('--')
                        display_dict[key+"_ref"].append('--')


                #Derived parameters from position (and DM)

                elif key=="l":
                     l_val = np.round(c_gal.l.deg,2)
                     if len(str(l_val).split('.')[-1]) < 2:
                         l_str = str(l_val) + '0'
                     else:
                         l_str = str(l_val)
                     display_dict[key].append(l_str)
                     display_dict[key+"_ref"].append(rrat_toml["RA"]["ref"])

                elif key=="b":
                     b_val = np.round(c_gal.b.deg,2)
                     if len(str(b_val).split('.')[-1]) < 2:
                         b_str = str(b_val) + '0'
                     else:
                         b_str = str(b_val)
                     display_dict[key].append(b_str)
                     display_dict[key+"_ref"].append(rrat_toml["Dec"]["ref"])

                #Nested dictionaries

                elif key=="BurstRate":
                    try:
                        z=rrat_toml[key]
                        try:
                            z=rrat_toml[key]["Discovery"]["value"]
                            display_dict[key].append(z)
                            display_dict[key+"_ref"].append(rrat_toml[key]["Discovery"]["ref"])
                        except:
                            vprint('One entry in BurstRate needs to be Discovery!')
                    except KeyError:
                        display_dict[key].append('--')
                        display_dict[key+"_ref"].append('--')


                elif key=="Width" or key=="Flux":
                    try:
                        z = rrat_toml[key]["1400"]["value"]
                        display_dict[key].append(z)
                        display_dict[key+"_ref"].append(rrat_toml[key]["1400"]["ref"])
                    except KeyError:
                        display_dict[key].append('--')
                        display_dict[key+"_ref"].append('--')

                else:
                    display_dict[key].append('--')
                    display_dict[key + "_ref"].append('--')


            display_df = pd.DataFrame(display_dict)
            full_display_df = pd.concat([full_display_df,display_df],ignore_index=True)

        except toml.decoder.TomlDecodeError as exc:
            vprint(rrat)
            vprint(exc)
            pass

    #print(full_display_df)

##########
#Output
##########

    if make_csv==True:
        full_display_df.to_csv('rratalog.csv',columns=df_keys)

    if make_html==True:
        display_df = full_display_df.drop(full_display_df.iloc[:,17:],axis=1)
        templateLoader = jinja2.FileSystemLoader(searchpath='./')
        env = jinja2.Environment(loader=templateLoader,trim_blocks=True,lstrip_blocks=True)
        template = env.get_template('template.html')
        with open("rratalog.html", "w") as fh:
            out = template.render(header=unit_keys, tableinfo=table_keys, df=full_display_df)
            fh.write(out)

    if make_tex==True:
        full_display_df.to_latex(buf='rratalog.tex',index=False)
