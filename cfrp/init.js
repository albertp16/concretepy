const input_data = require(`${__dirname}\\input.json`); //insert data here
//--> Design development... 
//--> Generate Carbon Fiber Analysis 

report_output = ``
report_output += `
\\documentclass{article}
\\usepackage[sfdefault]{roboto} %Using font stype
\\usepackage{graphicx} % Required for inserting images
\\usepackage[a4paper, total={7in, 10in}]{geometry}

\\title{Carbon Fiber Analysis}
\\author{Albert C Pamonag, m.Eng}
\\date{July 2023}
`

report_output += `
\\begin{document}
`

class flexureCFRP{
    constructor(data){
        this.data = data
    }
    inputs(){
        var report_init = `
        \\begin{center}
        \\begin{tabular}{|c | c | c |} 
        \\hline \n
        Description & Notations & Value\\\\ [0.5ex]  \n
        \\hline \n
        Beam Width & $b$ &  ${this.data["b"].toFixed(2)} mm \\\\ \n
        \\hline \n
        Beam Height & $h$ &  ${this.data["h"].toFixed(2)} mm \\\\ \n
        \\hline \n
        No. of bars & $n_{bot}$ &  ${this.data["n_bot"].toFixed(2)} \\\\ \n
        \\hline \n 
        Dia. of Main & $\\phi_{db}$ &  ${this.data["db"].toFixed(2)} mm \\\\ \n
        \\hline \n
        Dia. of Stirrups & $\\phi_{s}$ & ${this.data["dbs"].toFixed(2)} mm \\\\ \n
        \\hline \n
        Modulus Elasticity (Steel) & $E_{s}$ & ${this.data["Es"].toFixed(2)} GPa\\\\ \n
        \\hline \n
        \\end{tabular}
        \\end{center}


        \\subsection{CFRP Properties}

        \\begin{center}
        \\begin{tabular}{|c | c | c |} 
        \\hline
        Description & Notations & Value\\\\ [0.5ex] 
        \\hline
        Thickness per ply & $t_{f}$ &  ${this.data["frp"]["tf"].toFixed(2)} mm \\\\ \n
        \\hline \n
        Width of sheet & $w_{f}$ &  ${this.data["frp"]["w"].toFixed(2)} mm \\\\ \n
        \\hline
        Number of plies & $n$ &  ${this.data["frp"]["n"].toFixed(2)} plies \\\\ \n
        \\hline \n
        Ultimate tensile strength & $f^{*}_{fu}$ & ${this.data["frp"]["ffu"].toFixed(2)} MPa \\\\ \n
        \\hline \n
        Rupture strain & $\\epsilon^{*}_{fu}$ & ${input_data["frp"]["efu"].toFixed(2)} $\\frac{mm}{mm}$ \\\\ \n
        \\hline \n
        Modulus of Elasticity of FRP laminates & $E_{f}$ & ${this.data["frp"]["Ef"].toFixed(2)} GPa \\\\ \n 
        \\hline \n
        \\end{tabular}
        \\end{center}

        \\subsection{Loads}
        \\subsubsection{Corresponding Existing Moments}
        \\begin{center}
        \\begin{tabular}{|c | c | c |} 
        \\hline
        Description & Notations & Value\\\\ [0.5ex] 
        \\hline
        Service Moment (Dead) & $M_{dl,e}$ &  ${this.data["loads"]["existing"]["dl"].toFixed(2)} kN-m \\\\
        \\hline
        Service Moment (Live) & $M_{ll,e}$ &  ${this.data["loads"]["existing"]["ll"].toFixed(2)} kN-m \\\\
        \\hline
        \\end{tabular}
        \\end{center}

        \\subsubsection{Corresponding Anticipated Moments}
        \\begin{center}
        \\begin{tabular}{|c | c | c |} 
        \\hline
        Description & Notations & Value\\\\ [0.5ex] 
        \\hline
        Service Moment (Dead) & $M_{dl,a}$ &  ${this.data["loads"]["anticipated"]["dl"].toFixed(2)} kN-m  \\\\
        \\hline
        Service Moment (Live) & $M_{ll,a}$ &  ${this.data["loads"]["anticipated"]["ll"].toFixed(2)} kN-m  \\\\
        \\hline
        \\end{tabular}
        \\end{center}
        `
        return report_init
    }
    existingBeam(){
    }
    loadLimit(){
        function loadCombo(dle, lle, dla, lla) {
            //corresponding existing moment
            var mse = dle + lle
            var mue = 1.2 * dle + 1.6 * lle
            //corresponding anticipated moments 
            var msa = dla + lla
            var umla = 1.1 * dla + 0.75 * lla
            var mua = 1.2 * dla + 1.6 * lla
        
            return {
                "existing": {
                    "service": mse,
                    "factor": mue
                },
                "anticipated": {
                    "service": msa,
                    "unstrength_limit": umla,
                    "factor": mua
                }
            }
        
        }

        var actual_mu = 359.55 //TODO 

        var moment_loads = loadCombo(input_data["loads"]["existing"]["dl"],
        input_data["loads"]["existing"]["ll"],
        input_data["loads"]["anticipated"]["dl"],
        input_data["loads"]["anticipated"]["ll"])        
        var report_init = `
        \\subsection{Check for strengthening limit criteria as per ACI 440.2R-17:}
        $$ \\left( \\phi R_{n} \\right)_{existing} \\geq \\left( 1.1 S_{DL} + 0.75 S_{LL}\\right)$$
        $$ ${actual_mu.toFixed(2)}  kN-m \\geq  ${moment_loads["anticipated"]["unstrength_limit"].toFixed(2)}  kN-m $$        
        `

        return report_init
    }
    frpProp(){
        var report_output = ``
        report_output += `\\subsection{Computation the FRP system design material properties :}`
        report_output += `
        \\begin{flushleft}
        Table 1 presents the environmental reduction factor in accordance to ACI 440.2R-17
        \\end{flushleft}
        `
        function eRFTable() {
        
            report_output += `
            \\begin{table}[h!]
            \\centering
            \\begin{tabular}{|c | c | c | c | } 
            \\hline
            Description & Interior & Exterior & Aggressive\\\\ [0.5ex] 
            \\hline
            Carbon & 0.95 & 0.75 &  0.85 \\\\
            \\hline
            Glass & 0.85 & 0.65 &  0.75 \\\\
            \\hline
            Aramid & 0.85 & 0.50 &  0.70 \\\\
            \\hline
            \\end{tabular}
            \\caption{Environmental reduction factor for various FRP systems and exposure conditions}
            \\end{table}
            `
        }
        
        eRFTable()
        
        function eRF(exposure, type) {
            /*
            exposure [interior,Exterior,Aggressive]
            type [carbon,glass,aramid]
            */
            const data = {
                "interior": {
                    "carbon": 0.95,
                    "glass": 0.75,
                    "aramid": 0.85
                },
                "exterior": {
                    "carbon": 0.85,
                    "glass": 0.65,
                    "aramid": 0.75
                },
                "aggressive": {
                    "carbon": 0.85,
                    "glass": 0.50,
                    "aramid": 0.70
                },
            }
        
            var results = data[exposure][type]
            return results
        }
        
        var ffu = eRF(input_data['exposure']['condition'], input_data['exposure']['fiber']) * input_data['frp']['ffu']
        report_output += `\\subsubsection{Design Ultimate Tensile Strength of FRP}`
        report_output += `$$ f_{fu} = C_{E} f_{fu}^{*} $$ \n`
        report_output += `$$ f_{fu} = ${eRF(input_data['exposure']['condition'], input_data['exposure']['fiber'])} \\times ${input_data['frp']['ffu']} \\frac{N}{mm^{2}} $$ \n`
        report_output += `$$ f_{fu} = ${ffu.toFixed(2)} \\frac{N}{mm^{2}} $$ \n`
        
        var efu = eRF(input_data['exposure']['condition'], input_data['exposure']['fiber']) * input_data['frp']['efu']
        report_output += `\\subsubsection{Design Rupture Strain of FRP reinforcement attained at failure} \n`
        report_output += `$$ \\varepsilon_{fu} = C_{E} \\varepsilon_{fu}^{*} $$ \n`
        report_output += `$$ \\varepsilon_{fu} = ${eRF(input_data['exposure']['condition'], input_data['exposure']['fiber'])} \\times ${input_data['frp']['efu']} \\frac{mm}{mm} $$ \n`
        report_output += `$$ \\varepsilon_{fu} = ${efu.toFixed(6)} \\frac{mm}{mm} $$ \n`  

        return report_output
    }
}

report_output += `
\\maketitle
\\section{Inputs}
\\subsection{Material and Geometric Properties}
`

var flexure_output = new flexureCFRP(input_data)
report_output += flexure_output.inputs()

report_output += `
\\newpage 
\\section{Computations}
\\subsection{Check for Existing Beam Parameters :} 
`
report_output += `\\subsubsection{Effective depth} \n`
report_output += `\\subsubsection{$\\Beta _{1}$} \n`
report_output += `\\subsubsection{Actual Ratio} \n`

report_output += flexure_output.loadLimit()
report_output += flexure_output.frpProp()

// report_output += `\\subsection{Computation the FRP system design material properties :}`
// function eRFTable() {

//     report_output += `\\begin{center}
//     \\begin{tabular}{|c | c | c | c | } 
//     \\hline
//     Description & Interior & Exterior & Aggressive\\\\ [0.5ex] 
//     \\hline
//     Carbon & 0.95 & 0.75 &  0.85 \\\\
//     \\hline
//     Glass & 0.85 & 0.65 &  0.75 \\\\
//     \\hline
//     Aramid & 0.85 & 0.50 &  0.70 \\\\
//     \\hline
//     \\end{tabular}
//     \\end{center}
//     `
// }

// eRFTable()

// function eRF(exposure, type) {
//     /*
//     exposure [interior,Exterior,Aggressive]
//     type [carbon,glass,aramid]
//     */
//     const data = {
//         "interior": {
//             "carbon": 0.95,
//             "glass": 0.75,
//             "aramid": 0.85
//         },
//         "exterior": {
//             "carbon": 0.85,
//             "glass": 0.65,
//             "aramid": 0.75
//         },
//         "aggressive": {
//             "carbon": 0.85,
//             "glass": 0.50,
//             "aramid": 0.70
//         },
//     }

//     var results = data[exposure][type]
//     return results
// }

// var ffu = eRF(input_data['exposure']['condition'], input_data['exposure']['fiber']) * input_data['frp']['ffu']
// report_output += `\\subsubsection{Design Ultimate Tensile Strength of FRP}`
// report_output += `$$ f_{fu} = C_{E} f_{fu}^{*} $$ \n`
// report_output += `$$ f_{fu} = ${eRF(input_data['exposure']['condition'], input_data['exposure']['fiber'])} \\times ${input_data['frp']['ffu']} \\frac{N}{mm^{2}} $$ \n`
// report_output += `$$ f_{fu} = ${ffu.toFixed(2)} \\frac{N}{mm^{2}} $$ \n`

// var efu = eRF(input_data['exposure']['condition'], input_data['exposure']['fiber']) * input_data['frp']['efu']
// report_output += `\\subsubsection{Design Rupture Strain of FRP reinforcement attained at failure} \n`
// report_output += `$$ \\varepsilon_{fu} = C_{E} \\varepsilon_{fu}^{*} $$ \n`
// report_output += `$$ \\varepsilon_{fu} = ${eRF(input_data['exposure']['condition'], input_data['exposure']['fiber'])} \\times ${input_data['frp']['efu']} \\frac{mm}{mm} $$ \n`
// report_output += `$$ f_{fu} = ${efu.toFixed(6)} \\frac{mm}{mm} $$ \n`

report_output += `
\\subsection{Preliminary Calculations}
`
function beta_1(fc) {
    //NSCP 2015 422.2.2.4.3
    // var value = 1.05 - 0.05*(fc/1000)
    if (17 <= fc <= 28) {
        value = 0.85
    } else if (28 <= fc < 55) {
        value = 0.85 - ((0.05 * (fc - 28)) / 7)
    } else {
        value = 0.65
    }

    return value

}
function areaCircle(db) {
    var value = (Math.PI / 4) * (Math.pow(db, 2))
    return value
}
function modulusConcrete(fc) {
    return 4700 * Math.sqrt(fc)
}

var beta1 = beta_1(input_data['fc'])
var ec = modulusConcrete(input_data['fc']) //4700*Math.sqrt(input_data['fc'])
var n_bot = 3
var n_frp = 2
var as = n_bot * areaCircle(input_data['db'])
var af = n_frp * input_data["frp"]['tf'] * input_data['frp']['w']

report_output += `\\subsubsection{Properties of the concrete:} \n`
report_output += `$$ \\beta _{1} = ${beta1.toFixed(2)} $$ \n`

report_output += `\\subsubsection{Modulus of Elascity of Concrete} \n`
report_output += `$$ E_{c} = 4700 \\times \\sqrt{${input_data['fc']}} $$ \n`
report_output += `$$ E_{c} = ${ec.toFixed(2)} \\frac{N}{mm^{2}} $$ \n`


report_output += `\\subsubsection{Properties of the existing reinforcing steel}`
report_output += `$$ A_{s} = n_{bot} \\times db_{area} $$ \n`
report_output += `$$ A_{s} = ${n_bot} \\times ${areaCircle(input_data['db']).toFixed(2)} $$ \n`
report_output += `$$ A_{s} = ${as.toFixed(2)} mm^{2} $$ \n`

report_output += `\\subsubsection{Properties of the externally bonded FRP reinforcements} \n`
report_output += `$$ A_{f} = n_{frp} \\times t_{f} \\times b $$ \n`
report_output += `$$ A_{f} = ${n_frp} \\times ${input_data["frp"]['tf']} \\times ${input_data['frp']['w']} $$ \n`
report_output += `$$ A_{f} = ${af.toFixed(2)} mm^{2} $$ \n`



report_output += `
\\subsection{Determine the existing state of strain on the soffit} \n
`

var k = 0.334

var Icr = 2.471e6 //mm4 TODO double check this one
var df = input_data['h']
var d = input_data['d']
var MDL = 97.6
var ec_convert = ec / 1000
var ebi = (MDL * (df - (k * d))) / (Icr * ec_convert)

report_output += `$$ \\epsilon_{bi} = \\frac{ M _{DL} \\times \\left( d_{f} - kd \\right) }{ I_{cr} \\times E_{c} } $$ \n`
report_output += `$$ \\epsilon_{bi} = \\frac{ ${MDL.toFixed(2)} \\times \\left( ${df.toFixed(2)} - ${k.toFixed(2)} \\times ${d.toFixed(2)} \\right) }{ ${Icr.toFixed(2)} \\times ${ec_convert.toFixed(2)} } $$ \n`
report_output += `$$ \\epsilon_{bi} = ${ebi.toFixed(10)} $$ \n`

report_output += `
\\subsection{Determine the design strain of the FRP system} \n
`

var efd_init = input_data['fc'] / (2 * input_data["frp"]['tf'] * input_data["frp"]['Ef'])
var efd = 0.41 * Math.sqrt(efd_init)

report_output += `$$ \\epsilon _{fd} = 0.41 \\times \\sqrt{ \\frac{ f_{c}^{'} }{ 2 \\times E_{f} \\times t_{f} } } $$ \n`
report_output += `$$ \\epsilon _{fd} = 0.41 \\times \\sqrt{ \\frac{ ${input_data['fc']} }{ 2 \\times ${input_data["frp"]['tf']} \\times ${input_data["frp"]['Ef']} } } $$ \n`
report_output += `$$ \\epsilon _{fd} = ${efd.toFixed(3)} $$ \n`

report_output += `
\\subsection{Computation of the compression block}
Assume "$c = 0.20 \\times d$" as initital inputs`

function cSolver() { //Numerical Solver

    //--> Data for the tabulations
    var epsilon_fe_arr = []
    var espilon_c_arr = []
    var eespilon_s_arr = []
    var e_c_prime_arr = []
    var beta_one_arr = []
    var alpha_one_arr = []
    var c_init_arr = []

    let c_init = 0.20 * input_data['d']

    for (var i = 1; i <= 20; i++) {
        // console.log(c_init)

        epsilon_fe = 0.003 * ((input_data['h'] - c_init) / c_init) - ebi
        espilon_c = (0.009 + ebi) * (c_init / (input_data['h'] - c_init))
        espilon_s = (0.009 + ebi) * ((input_data['d'] - c_init) / (input_data['h'] - c_init))

        let fs = input_data['Es'] * espilon_s
        fs = input_data['fy']//414 //TODO fix on the yields

        f_fe = input_data['frp']['Ef'] * 0.009

        e_c_prime = 1.7 * input_data['fc'] / ec
        beta_one = ((4 * e_c_prime) - espilon_c) / ((6 * e_c_prime) - (2 * espilon_c))
        alpha_one = ((3 * e_c_prime * espilon_c) - Math.pow(espilon_c, 2)) / (3 * beta_one * Math.pow(e_c_prime, 2))
        c_init = (as * fs + af * f_fe) / (alpha_one * input_data['fc'] * beta_one * input_data['frp']['w'])

        epsilon_fe_arr.push(epsilon_fe)
        espilon_c_arr.push(espilon_c)
        eespilon_s_arr.push(espilon_s)
        e_c_prime_arr.push(e_c_prime)
        beta_one_arr.push(beta_one)
        alpha_one_arr.push(alpha_one)
        c_init_arr.push(c_init)



    }
    c = c_init

    var results = {
        "value": c,
        "epsilon_fe": epsilon_fe_arr,
        "espilon_c": espilon_c_arr,
        "espilon_s": eespilon_s_arr,
        "e_c_prime": e_c_prime_arr,
        "beta_one": beta_one_arr,
        "alpha_one": alpha_one_arr,
        "c_init": c_init_arr,
    }

    return results

}

var c_data = cSolver()

report_output += `
\\begin{center}
\\begin{tabular}{|c | c | c | c | c | c | c |} 
\\hline
c & $\\epsilon_{fe}$ & $\\epsilon_{c}$ & $\\epsilon_{s}$ & $\\epsilon^{'}_{c}$ & $\\beta_{1}$ & $\\alpha_{1}$ \\\\ [0.5ex] 
\\hline`

for (var i = 0; i < c_data["c_init"].length; i++) {
    report_output += `${c_data["c_init"][i].toFixed(2)} & ${c_data["epsilon_fe"][i].toFixed(4)} & ${c_data["espilon_c"][i].toFixed(4)} & ${c_data["espilon_s"][i].toFixed(4)} & ${c_data["e_c_prime"][i].toFixed(4)} & ${c_data["beta_one"][i].toFixed(4)} & ${c_data["alpha_one"][i].toFixed(4)} \\\\ \n
    \\hline
    `
}

report_output += `
\\end{tabular}
\\end{center}
`


report_output += `
\\subsection{Computation of Flexural Strength}
`

var n_length = c_data["beta_one"].length
var beta_one_final = c_data["beta_one"][n_length - 1]

//Computation Steel Contribution to Bending
var fs = 414 //--> to review soon
var As = as
var Af = af
var Mns = As * fs * (input_data['d'] - ((beta_one_final * c_data['c_final']) / 2))

var f_fe = input_data['frp']['Ef'] * 0.009
//Computation FRP contribution to bending
report_output += `\\subsubsection{Computation Steel Contribution to Bending} \n`
// report += `<h4>FRP contribution to bending</h4>`
var Mnf = Af * f_fe * (input_data["h"] - (beta_one_final * c_data['c_final']) / 2)
// console.log(Mnf/1e6)

// report += `<h4>Computation of design flexural strength of the section</h4>`
var psi_f = 0.85 //research 
var phi_b = 0.90
var phiMn = phi_b * (Mns + (psi_f * Mnf))
report_output += `$$ \\phi M_{n} = \\phi \\left[ M_{ns} + \\psi_{f} M_{nf} \\right] $$`

report_output += `$$ \\phi M_{n} = ${(phiMn / 1e6).toFixed(3)} $$`


function rho(As, b, d) {
    var value = As / (b * d)
    return value
}

var rho_s = rho(as, input_data["h"], input_data["w"])
var rho_f = rho(af, input_data["h"], input_data["w"])

report_output += `\\subsection{Calculate service stresses in reinforcing steel and the FRP} \n`
var Es = 200
var Ec = ec / 1000
var Ef = input_data['frp']['Ef'] / 1000

var k1 = Math.pow(rho_s * (Es / Ec) + rho_f * (Ef / Ec), 2)
var k2 = 2 * (rho_s * (Es / Ec) + rho_f * (Ef / Ec) * (input_data['h'] / input_data['d']))
var k3 = rho_s * (Es / Ec) + rho_f * (Ef / Ec)

var k = Math.sqrt(k1 + k2) - k3

var k1_latex = `\\left( \\rho_{s} \\frac{E_{s}}{E_{c}} + \\rho_{f} \\frac{E_{f}}{E_{c}} \\right)^{2}`
var k2_latex = `2.0 \\times \\left[ \\rho_{s} \\frac{E_{s}}{E_{c}} + \\rho_{f} \\frac{E_{f}}{E_{c}} \\times \\left( \\frac{d_{f}}{d} \\right) \\right]`
var k3_latex = `\\left( \\rho_{s} \\frac{E_{s}}{E_{c}} + \\rho_{f} \\frac{E_{f}}{E_{c}} \\right)`

report_output += `$$ k = \\sqrt{ ${k1_latex} + ${k2_latex} } - ${k3_latex} $$ \n`
report_output += `$$ k =  ${k.toFixed(4)} $$`


report_output += `
\\end{document}
`

console.log(report_output)



