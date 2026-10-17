function bioleaching_model
% BIOLEACHING_MODEL  Coupled TetH / thiosulfate / gold / copper leaching model.
%
%   Single-file implementation of the model chain in "Bioleaching Modelling -
%   Process Overview":
%       1. Enzyme (TetH) production
%       2. Tetrathionate consumption (Michaelis-Menten + Cu(II) regeneration)
%       3. Thiosulfate production and losses
%       4. Gold leaching    - Model A (O2 only) or Model B (O2 + Cu(II))
%       5. Copper leaching and the Cu(I)/Cu(II) balance
%       6. pH               - stub, see the marked block in rhs()
%
%   Everything is in this one file as local functions, so there is nothing to
%   add to the path and no per-call file lookup.
%
%   USAGE
%       >> bioleaching_model          % baseline run, sweeps, model comparison
%
%   TO CHANGE A PARAMETER PERMANENTLY   -> edit default_params() below.
%   TO SEE THE EFFECT OF CHANGING ONE   -> use the SWEEP BLOCKS in the main
%                                          body; copy a line, change the field
%                                          name and the values.
%
%   UNITS
%       concentrations  umol L^-1        solid metal      umol
%       areas           m^2              time             min
%       surface rates   umol min^-1      bulk rates       umol L^-1 min^-1
%
%   STATE VECTOR y
%       1 [E]        TetH enzyme                 6 n_Cu       solid copper
%       2 [S4O6^2-]  tetrathionate               7 [Cu(I)]
%       3 [S2O3^2-]  thiosulfate                 8 [Cu(II)]
%       4 n_Au       solid gold                  9 [O2]
%       5 [Au(S2O3)2^3-] dissolved gold         10 [H+]      (pH stub)

clc; close all;

%% ------------------------------------------------------------------
%  BASELINE RUN
%  ------------------------------------------------------------------
p = default_params();
p = refresh(p);

[t, Y, aux] = run_model(p);
plot_run(t, Y, aux, p, sprintf('Baseline - Model %s', p.gold_model));

print_summary(t, Y, aux, p);

%% ------------------------------------------------------------------
%  SWEEP BLOCKS  -  "change a parameter and look at it again"
%  ------------------------------------------------------------------
%  TEMPLATE:
%      sweep(p, 'field_name', [v1 v2 v3], 'plot_key')
%
%  'field_name' is any field in default_params().
%  'plot_key' selects the y-axis. Available keys:
%      'Au_recovery'  'Cu_recovery'  'Au_dissolved'  'Cu_dissolved'
%      'S2O3'  'S4O6'  'E'  'CuI'  'CuII'  'O2'  'n_Au'  'n_Cu'
%      'R_Au'  'R_Cu'  'R_Au_O2'  'R_Au_Cu'  'A_Cu'  'pH'
%      'fS'  'fO2'  'fCu'                (saturation factors, 0-1)
%
%  Comment out the ones you do not want; add your own underneath.
%  ------------------------------------------------------------------

% --- the three that matter most, ON by default ----------------------
%sweep(p, 'k_cat',  [30 125 400],          'Au_recovery');  % enzyme turnover: Low/Base/High
%sweep(p, 'F_in',   [0.25 1 4],            'S2O3');         % feed rate vs enzyme capacity
%sweep(p, 'k1',     [1e-6 1e-5 1e-4],      'S2O3');         % parasitic loss (no-ammonia risk)

% --- uncomment as needed --------------------------------------------
%sweep(p, 'k4',      [1e-5 1e-4 1e-3],     'CuII');          % Cu(I) re-oxidation
%sweep(p, 'O2',      [50 150 250 400],     'Au_recovery');   % aeration
%sweep(p, 'd',       [2e-3 4e-3 6e-3],     'Cu_recovery');   % crush size
%sweep(p, 't_film',  [0.05e-6 0.5e-6 1e-6],'Au_recovery');   % plating thickness
%sweep(p, 'K_S',     [1e4 5e4 2e5],        'Au_recovery');   % S2O3 half-saturation
%sweep(p, 'X',       [1e11 1e12 1e13],     'Au_recovery');   % biomass loading

% Two parameters at once (recovery at the end of the run, as a surface):
%sweep2(p, 'F_in', [0.25 0.5 1 2 4], 'k_cat', [30 60 125 250 400], 'Au_recovery');

% Model A vs Model B, same parameters, same axes:
compare_gold_models(p);

end % ======================= end of main =======================


%% ===================================================================
%  PARAMETERS  -  EDIT HERE
%  ===================================================================
function p = default_params()

% ---- operating / reactor -------------------------------------------
p.V          = 1.0;        % L        reactor volume
p.t_end      = 3*24*60;    % min      simulated time (3 days)
p.gold_model = 'B';        % 'A' = O2 only, 'B' = O2 + Cu(II)
p.stoich     = 'split';    % 'split' = pathway-resolved (recommended)
                           % 'doc'   = exactly as typed in the write-up
                           %           (see the NOTE in rhs - 'doc' drives
                           %            Cu(II) negative)

% ---- 1. enzyme ------------------------------------------------------
%  k_syn is set so the steady state matches the gene-expression cascade:
%     E_ss = k_syn*X/(k_deg+mu) = 4.75e-3 umol/L = ~2900 TetH molecules/cell,
%  which is a realistic burden (an E. coli cell holds ~3e6 proteins in total).
%  The previous value (1e-13) implied 5.5e7 molecules/cell - 18x more protein
%  than the entire cell contains.
p.X       = 1e12;      % cell L^-1        biomass, held constant (chemostat)
p.k_syn   = 8.74e-17;  % umol cell^-1 min^-1  synthesis   [cascade-matched, ref 17]
p.k_deg   = 1.1e-3;    % min^-1           enzyme degradation      [ref 4]
p.mu      = 0.0173;    % min^-1           growth dilution = ln2/40min [ref 16]

% ---- 2. tetrathionate ------------------------------------------------
%  F_in is matched to the enzyme's capacity. V_max = k_cat*E_ss = 0.59
%  umol/L/min, so feeding much faster than that just piles up unused
%  substrate (the old F_in = 20 was ~34x the enzyme's throughput).
p.F_in    = 0.0;       % umol L^-1 min^-1  S4O6 feed (0 = batch)
p.k_cat   = 125;       % min^-1            TetH turnover: 2.5 U/mg x 50 kDa [ref 1,2]
p.Km      = 300;       % umol L^-1         Michaelis constant, 50-2400 [ref 2]
p.k1      = 1e-5;      % L umol^-1 min^-1  Cu(II)+S2O3 -> S4O6    [ref 6,7]

% ---- 3. thiosulfate --------------------------------------------------
p.Y       = 1;         % -                 S2O3 per S4O6 consumed    [ref 1]

% ---- 4. gold ---------------------------------------------------------
%  Feed basis: 100 g/L PCB (10 % pulp density) at a typical assay of
%  0.02 wt% Au and 30 wt% Cu  ->  20 mg Au and 30 g Cu per litre.
%  The old values (0.2 g Au + 100 g Cu) implied a 33 % pulp density and a
%  0.06 wt% gold assay, i.e. 3x richer than a real board.
p.m_Au    = 20e-6;     % kg                gold on the boards (20 mg)
p.rho_Au  = 19300;     % kg m^-3                                    [doc]
p.t_film  = 0.5e-6;    % m                 plating thickness, 0.05-1 um
p.k_Au_O2 = 11.4;      % umol m^-2 min^-1  O2 route (1.9e-7 mol/m2/s) [ref 9,10]
p.k_Au_Cu = 1500;      % umol m^-2 min^-1  Cu(II) route (PCB optimum) [ref 11,12]
p.K_O2    = 50;        % umol L^-1         O2 half-saturation       [ref 10]
p.K_S     = 3900;       % umol L^-1         S2O3 half-saturation     [ref 11]
%  K_Cu must be large: gold leaching stays FIRST ORDER in Cu(II) up to
%  ~0.15 M (1.5e5 umol/L), so half-saturation sits at or above that scale.
%  The old value (500) made the Cu term saturate at trace copper.
p.K_Cu    = 5e4;       % umol L^-1         Cu(II) half-saturation   [ref 12]

% ---- 5. copper -------------------------------------------------------
p.m_Cu    = 30e-3;     % kg                copper mass (30 g = 30 wt% of 100 g)
p.rho_Cu  = 8960;      % kg m^-3                                    [doc]
p.d       = 6e-3;      % m                 crushed particle size, 2-6 mm
p.k_Cu_O2 = 200;       % umol m^-2 min^-1  O2 route (Ea ~25.8 kJ/mol) [ref 13]
p.k_Cu_Cu = 200;       % umol m^-2 min^-1  Cu(II) route (comproportionation)
p.k3      = 1e-5;      % L umol^-1 min^-1  parasitic, = k1          [ref 6,7]
p.k4      = 1e-4;      % L umol^-1 min^-1  Cu(I) re-oxidation       [ref 7]

% ---- oxygen -----------------------------------------------------------
p.O2_mode = 'fixed';   % 'fixed' = sparged/saturated, 'mtc' = kLa-limited
p.O2      = 500;       % umol L^-1         dissolved O2 (~8 mg/L, air-sat)
p.kLa     = 0.5;       % min^-1            only used when O2_mode = 'mtc'

% ---- 6. pH -------------------------------------------------------------
p.pH_on   = false;      % proton balance is now written (see rhs)
p.beta    = 1e3;       % umol L^-1         buffer capacity   [CALIBRATE]

% ---- initial coditions -------------------------------------------------
p.M_Au = 196.97e-3;    % kg mol^-1   used only to convert kg metal -> umol
p.M_Cu = 63.55e-3;     % kg mol^-1

p.y0 = [ 0                            ;  % 1  [E]
         23200                            ;  % 2  [S4O6]
         72100                            ;  % 3  [S2O3]
         p.m_Au / p.M_Au * 1e6        ;  % 4  n_Au   (umol solid)
         0                            ;  % 5  [Au(S2O3)2]
         p.m_Cu / p.M_Cu * 1e6        ;  % 6  n_Cu   (umol solid)
         0                            ;  % 7  [Cu(I)]
         0                            ;  % 8  [Cu(II)]
         p.O2                         ;  % 9  [O2]
         0.1                          ]; % 10 [H+] umol/L = 1e-7 M -> pH 7.0
                                         %    (old 1e-2 umol/L was pH 8, not 4)
end


%% ===================================================================
%  SOLVER WRAPPER
%  ===================================================================
function [t, Y, aux] = run_model(p)

p = refresh(p);          % rebuild derived constants + initial conditions

opts = odeset('RelTol', 1e-7, 'AbsTol', 1e-9, ...
              'NonNegative', 1:numel(p.y0));

[t, Y] = ode15s(@(tt,yy) rhs(tt, yy, p), [0 p.t_end], p.y0, opts);

% Recompute the algebraic quantities along the solution, for plotting.
n = numel(t);
z = zeros(n,1);
aux = struct('A_Au',z, 'A_Cu',z, 'R_Au',z, 'R_Cu',z, 'v_MM',z, 'pH',z, ...
             'fS',z, 'fO2',z, 'fCu',z, 'R_Au_O2',z, 'R_Au_Cu',z);
for i = 1:n
    [~, a] = rhs(t(i), Y(i,:).', p);
    aux.A_Au(i) = a.A_Au;   aux.A_Cu(i) = a.A_Cu;
    aux.R_Au(i) = a.R_Au;   aux.R_Cu(i) = a.R_Cu;
    aux.v_MM(i) = a.v_MM;   aux.pH(i)   = a.pH;
    aux.fS(i)   = a.fS;     aux.fO2(i)  = a.fO2;   aux.fCu(i) = a.fCu;
    aux.R_Au_O2(i) = a.R_Au_O2;  aux.R_Au_Cu(i) = a.R_Au_Cu;
end

aux.Au_recovery = 100 * (1 - Y(:,4) / p.nAu0);   % %
aux.Cu_recovery = 100 * (1 - Y(:,6) / p.nCu0);   % %
end


function p = refresh(p)
%REFRESH  Recompute everything that depends on the parameters.
%   Called before every run so that sweeping m_Au, t_film, d, O2 ... also
%   moves the initial conditions and the areas, not just the rate law.

% Gold is a thin plated film: it thins at roughly constant face area.
%   A = m / (rho * t_film)
p.A_Au0 = p.m_Au / (p.rho_Au * p.t_film);        % m^2

% Copper is bulk metal: shrinking particle, A(0) = 6m/(rho*d)
p.A_Cu0 = 6 * p.m_Cu / (p.rho_Cu * p.d);         % m^2

p.y0(4) = p.m_Au / p.M_Au * 1e6;                 % umol
p.y0(6) = p.m_Cu / p.M_Cu * 1e6;                 % umol
p.y0(9) = p.O2;

p.nAu0 = p.y0(4);
p.nCu0 = p.y0(6);
end


%% ===================================================================
%  RIGHT-HAND SIDE  -  the model itself
%  ===================================================================
function [dy, a] = rhs(~, y, p)

% ---- unpack (clamped: the solver can probe slightly negative) --------
E    = max(y(1) ,0);   S4   = max(y(2) ,0);   S2   = max(y(3) ,0);
nAu  = max(y(4) ,0);   AuC  = max(y(5) ,0);   nCu  = max(y(6) ,0); %#ok<NASGU>
CuI  = max(y(7) ,0);   CuII = max(y(8) ,0);   O2   = max(y(9) ,0);
H    = max(y(10),1e-12);

useCuII = strcmpi(p.gold_model, 'B');   % is the Cu(II) oxidant route active?

% ---- saturation (Langmuir) terms -------------------------------------
fO2 = O2   / (p.K_O2 + O2);
fS  = S2   / (p.K_S  + S2);
fCu = CuII / (p.K_Cu + CuII);

% ---- 1. ENZYME --------------------------------------------------------
%   d[E]/dt = k_syn*X - (k_deg + mu)*[E]
dE = p.k_syn * p.X - (p.k_deg + p.mu) * E;

% ---- 2. TETRATHIONATE -------------------------------------------------
v_MM = p.k_cat * E * S4 / (p.Km + S4);           % umol L^-1 min^-1
v3   = p.k3 * CuII * S2;                         % parasitic 2Cu(II)+2S2O3 -> S4O6
v4   = p.k4 * O2  * CuI;                         % 4Cu(I)+O2 -> 4Cu(II)

dS4 = p.F_in - v_MM + p.k1 * CuII * S2;

% ---- 4. GOLD: area and rate -------------------------------------------
% Thin film -> constant face area while gold remains, then 0. The smooth
% switch avoids a hard discontinuity that would stall the stiff solver.
A_Au = p.A_Au0 * smooth_step(nAu, 1e-4 * p.nAu0);

R_Au_O2 = p.k_Au_O2 * A_Au * fO2 * fS;                        % umol min^-1
R_Au_Cu = 0;
if useCuII
    R_Au_Cu = p.k_Au_Cu * A_Au * fS * fCu;                    % umol min^-1
end
R_Au = R_Au_O2 + R_Au_Cu;

dnAu = -R_Au;
dAuC =  R_Au / p.V;

% ---- 5. COPPER: area and rates ----------------------------------------
% Shrinking particle: A(t) = A(0) * (n/n0)^(2/3)
A_Cu = p.A_Cu0 * (nCu / p.nCu0)^(2/3) * smooth_step(nCu, 1e-4 * p.nCu0);

switch lower(p.stoich)

  case 'split'
    % --------------------------------------------------------------
    % Pathway-resolved form (recommended). Each oxidant route is kept
    % separate so that the stoichiometric coefficients land on the
    % species they actually belong to:
    %
    %   O2 route      4Cu0 + O2 + 8S2O3 -> 4[Cu(S2O3)2]3-
    %                 per Cu0: 1 Cu(I) made, 2 S2O3 used, 0 Cu(II) used
    %   Cu(II) route  Cu0 + Cu2+ + 4S2O3 -> 2[Cu(S2O3)2]3-
    %                 per Cu0: 2 Cu(I) made, 4 S2O3 used, 1 Cu(II) used
    % --------------------------------------------------------------
    v_Cu_O2 = p.k_Cu_O2 * A_Cu * fO2 * fS;       % umol Cu0 min^-1
    v_Cu_Cu = 0;
    if useCuII
        v_Cu_Cu = p.k_Cu_Cu * A_Cu * fS * fCu;   % umol Cu0 min^-1
    end
    R_Cu = v_Cu_O2 + v_Cu_Cu;
    R_Cu_O2 = v_Cu_O2;                           % exposed for the pH balance

    S2_from_Cu = (2 * v_Cu_O2 + 4 * v_Cu_Cu) / p.V;
    CuI_src    = (v_Cu_O2 + 2 * v_Cu_Cu) / p.V + R_Au_Cu / p.V;
    CuII_sink  =  v_Cu_Cu / p.V + R_Au_Cu / p.V;

    dCuI  =  CuI_src  + 2 * v3 - 4 * v4;
    dCuII =  4 * v4 - CuII_sink - 2 * v3;

  case 'doc'
    % --------------------------------------------------------------
    % Verbatim from the write-up. NOTE: as written, v1B is subtracted
    % from Cu(II) in full - including its oxygen-route part, which does
    % not consume Cu(II) - and v2 = R_Au is subtracted in full even
    % when gold is being leached by O2. Both drive [Cu(II)] negative.
    % Kept here so the code can be checked line-by-line against the
    % document; use 'split' for actual runs.
    % --------------------------------------------------------------
    v1A = 2 * p.k_Cu_O2 * A_Cu * fO2 * fS;
    v1B = A_Cu * fS * (2*p.k_Cu_O2*fO2 + 4*p.k_Cu_Cu*fCu);
    if useCuII, R_Cu = v1B; else, R_Cu = v1A; end
    v2  = R_Au;
    R_Cu_O2 = p.k_Cu_O2 * A_Cu * fO2 * fS;       % exposed for the pH balance

    S2_from_Cu = R_Cu / p.V;
    dCuI  = (1/p.V)*2*v1B + (1/p.V)*v2 + 2*v3 - 4*v4;
    dCuII =  4*v4 - (1/p.V)*v1B - (1/p.V)*v2 - 2*v3;

  otherwise
    error('p.stoich must be ''split'' or ''doc''.');
end

dnCu = -R_Cu;

% ---- 3. THIOSULFATE ----------------------------------------------------
%   made by TetH; lost to the parasitic Cu(II) reaction, to gold (2 per Au)
%   and to copper (2 or 4 per Cu, depending on the oxidant route)
dS2 = p.Y * v_MM ...
    - 2 * v3 ...
    - (2/p.V) * R_Au ...
    - S2_from_Cu;

% ---- OXYGEN -------------------------------------------------------------
switch lower(p.O2_mode)
    case 'fixed'
        dO2 = 0;                              % held at the sparged value
    case 'mtc'
        % 1/4 O2 per Au (O2 route), 1/4 per Cu (O2 route), 1/4 per Cu(I)
        O2_use = 0.25*(R_Au_O2/p.V) + 0.25*(R_Cu/p.V) + v4;
        dO2 = p.kLa * (p.O2 - O2) - O2_use;
    otherwise
        error('p.O2_mode must be ''fixed'' or ''mtc''.');
end

% =========================================================================
% ---- 6. pH  ================  IMPLEMENTED  ================  -----------
% =========================================================================
% Proton sources and sinks that follow from the reactions already written:
%
%   S4O6 hydrolysis      S4O6 + H2O -> S2O3 + S + SO4 + 2H+     +2 per v_MM
%   Au leach, O2 route   ... + O2 + 2H2O -> ... + 4OH-          -1 per Au
%   Cu leach, O2 route   ... + O2 + 2H2O -> ... + 4OH-          -1 per Cu
%   Cu(I) re-oxidation   4Cu(I) + O2 + 2H2O -> 4Cu(II) + 4OH-   -4 per v4
%
% All four terms are now written below. beta is a lumped buffer capacity:
% raise it to represent a buffered medium, lower it for an unbuffered one.
% Set p.pH_on = false to freeze pH instead.
%
if p.pH_on
    dH = ( 2 * v_MM ...                       % +2 H+ per S4O6 hydrolysed
         - R_Au_O2 / p.V ...                  % -1 H+ (1 OH-) per Au, O2 route
         - R_Cu_O2 / p.V ...                  % -1 H+ (1 OH-) per Cu, O2 route
         - 4 * v4 ...                         % -4 H+ (4 OH-) per Cu(I) re-ox
         ) / (1 + p.beta);
else
    dH = 0;
end
% =========================================================================

% ---- assemble ------------------------------------------------------------
dy = [dE; dS4; dS2; dnAu; dAuC; dnCu; dCuI; dCuII; dO2; dH];

if nargout > 1
    a = struct('A_Au',A_Au, 'A_Cu',A_Cu, 'R_Au',R_Au, 'R_Cu',R_Cu, ...
               'R_Au_O2',R_Au_O2, 'R_Au_Cu',R_Au_Cu, ...
               'v_MM',v_MM, 'v3',v3, 'v4',v4, ...
               'fS',fS, 'fO2',fO2, 'fCu',fCu, ...   % saturation factors (0-1)
               'pH', -log10(max(H,1e-12) * 1e-6));   % umol/L -> mol/L
end
end


%% ===================================================================
%  HELPERS
%  ===================================================================
function s = smooth_step(x, w)
%SMOOTH_STEP  ~0 when x <= 0, ~1 when x >> w. Keeps the stiff solver stable
%   at metal exhaustion instead of a hard if-statement.
if x <= 0
    s = 0;
else
    s = x / (w + x);
end
end


function out = get_series(Y, aux, key)
switch key
    case 'E',            out = Y(:,1);
    case 'S4O6',         out = Y(:,2);
    case 'S2O3',         out = Y(:,3);
    case 'n_Au',         out = Y(:,4);
    case 'Au_dissolved', out = Y(:,5);
    case 'n_Cu',         out = Y(:,6);
    case 'CuI',          out = Y(:,7);
    case 'CuII',         out = Y(:,8);
    case 'O2',           out = Y(:,9);
    case 'Cu_dissolved', out = Y(:,7) + Y(:,8);
    case 'Au_recovery',  out = aux.Au_recovery;
    case 'Cu_recovery',  out = aux.Cu_recovery;
    case 'R_Au',         out = aux.R_Au;
    case 'R_Cu',         out = aux.R_Cu;
    case 'A_Cu',         out = aux.A_Cu;
    case 'pH',           out = aux.pH;
    case 'fS',           out = aux.fS;
    case 'fO2',          out = aux.fO2;
    case 'fCu',          out = aux.fCu;
    case 'R_Au_O2',      out = aux.R_Au_O2;
    case 'R_Au_Cu',      out = aux.R_Au_Cu;
    otherwise
        error('Unknown plot key ''%s''. See the list in the sweep block.', key);
end
end


function lab = label_for(key)
switch key
    case {'Au_recovery','Cu_recovery'}, lab = 'recovery (%)';
    case {'R_Au','R_Cu'},               lab = 'rate (\mumol min^{-1})';
    case 'A_Cu',                        lab = 'area (m^2)';
    case 'pH',                          lab = 'pH';
    case {'fS','fO2','fCu'},            lab = 'saturation factor (0-1)';
    case {'n_Au','n_Cu'},               lab = 'solid metal (\mumol)';
    otherwise,                          lab = 'concentration (\mumol L^{-1})';
end
end


%% ===================================================================
%  PLOTTING
%  ===================================================================
function plot_run(t, Y, aux, p, ttl)
th = t / 60;                                    % hours

figure('Name', ttl, 'Color', 'w', 'Position', [60 60 1280 680]);

subplot(2,4,1);
plot(th, Y(:,1)*1e3, 'LineWidth', 1.5); grid on;
xlabel('time (h)'); ylabel('[E] (nmol L^{-1})'); title('(a) TetH enzyme');

subplot(2,4,2);
plot(th, Y(:,2), 'LineWidth', 1.5); hold on;
plot(th, Y(:,3), 'LineWidth', 1.5); grid on;
xlabel('time (h)'); ylabel('\mumol L^{-1}');
legend('S_4O_6^{2-}', 'S_2O_3^{2-}', 'Location', 'best');
title('(b) Sulfur species');

subplot(2,4,3);
plot(th, Y(:,8), 'LineWidth', 1.5); hold on;
plot(th, Y(:,7), '--', 'LineWidth', 1.5); grid on;
xlabel('time (h)'); ylabel('\mumol L^{-1}');
legend('Cu(II) - oxidant', 'Cu(I) - inactive', 'Location', 'best');
title('(c) Copper redox balance');

subplot(2,4,4);
plot(th, Y(:,5), 'LineWidth', 1.5); grid on;
xlabel('time (h)'); ylabel('\mumol L^{-1}');
title('(d) Dissolved gold Au(S_2O_3)_2^{3-}');

subplot(2,4,5);
plot(th, aux.Au_recovery, 'LineWidth', 1.5); hold on;
plot(th, aux.Cu_recovery, '--', 'LineWidth', 1.5); grid on;
xlabel('time (h)'); ylabel('recovery (%)');
legend('Au', 'Cu', 'Location', 'best'); title('(e) Metal recovery');

subplot(2,4,6);
plot(th, aux.R_Au, 'LineWidth', 1.5); hold on;
plot(th, aux.R_Au_O2, ':', 'LineWidth', 1.4);
plot(th, aux.R_Au_Cu, '-.', 'LineWidth', 1.4); grid on;
xlabel('time (h)'); ylabel('\mumol min^{-1}');
legend('total', 'O_2 route', 'Cu(II) route', 'Location', 'best');
title('(f) Gold leaching rate R_{Au}');

subplot(2,4,7);
plot(th, aux.fS, 'LineWidth', 1.5); hold on;
plot(th, aux.fO2, 'LineWidth', 1.5);
plot(th, aux.fCu, 'LineWidth', 1.5); grid on;
xlabel('time (h)'); ylabel('saturation factor (0-1)'); ylim([0 1]);
legend('f_S (thiosulfate)', 'f_{O2} (oxygen)', 'f_{Cu} (Cu(II))', 'Location', 'best');
title('(g) What is limiting the rate');

subplot(2,4,8);
plot(th, aux.pH, 'LineWidth', 1.5); grid on;
xlabel('time (h)'); ylabel('pH'); title('(h) pH');

if exist('sgtitle', 'file'), sgtitle(ttl, 'FontWeight', 'bold'); end
end


%% ===================================================================
%  SUMMARY PRINTOUT  -  sanity numbers for the baseline run
%  ===================================================================
function print_summary(t, Y, aux, p)
NA   = 6.022e17;                     % molecules per umol
E_ss = p.k_syn * p.X / (p.k_deg + p.mu);
Vmax = p.k_cat * E_ss;

fprintf('\n================ BASELINE SUMMARY (Model %s) ================\n', p.gold_model);
fprintf('Feed basis\n');
fprintf('   gold on boards        %8.1f umol L^-1  (%.0f mg)\n', p.nAu0, p.m_Au*1e6);
fprintf('   copper on boards      %8.0f umol L^-1  (%.0f g)\n',  p.nCu0, p.m_Cu*1e3);
fprintf('   Cu : Au molar ratio   %8.0f : 1\n',                   p.nCu0/p.nAu0);
fprintf('   gold area  A_Au       %8.3e m^2   (thin film, constant)\n', p.A_Au0);
fprintf('   copper area A_Cu(0)   %8.3e m^2   (shrinking particle)\n',  p.A_Cu0);

fprintf('\nEnzyme\n');
fprintf('   [E] steady state      %8.4g umol L^-1  = %.0f molecules/cell\n', ...
        E_ss, E_ss*NA/p.X);
fprintf('   V_max = k_cat*[E]     %8.4f umol L^-1 min^-1\n', Vmax);
fprintf('   F_in / V_max          %8.2f   (>1 means substrate piles up)\n', p.F_in/Vmax);

fprintf('\nEnd of run (t = %.0f h)\n', p.t_end/60);
fprintf('   thiosulfate           %8.0f umol L^-1  (peak %.0f = %.2f mM)\n', ...
        Y(end,3), max(Y(:,3)), max(Y(:,3))/1000);
fprintf('   Cu(II) / Cu(I)        %8.2f\n', Y(end,8)/max(Y(end,7),1e-9));
fprintf('   gold recovered        %8.3f %%\n', aux.Au_recovery(end));
fprintf('   copper dissolved      %8.4f %%\n', aux.Cu_recovery(end));
fprintf('   pH                    %8.2f\n', aux.pH(end));

fprintf('\nRate limitation at end of run (saturation factors, 1 = not limiting)\n');
fprintf('   f_S  thiosulfate      %8.4f  <-- the throttle if this is small\n', aux.fS(end));
fprintf('   f_O2 oxygen           %8.4f\n', aux.fO2(end));
fprintf('   f_Cu copper(II)       %8.4f\n', aux.fCu(end));
fprintf('   R_Au split: O2 %.0f %%, Cu(II) %.0f %%\n', ...
        100*aux.R_Au_O2(end)/max(aux.R_Au(end),1e-30), ...
        100*aux.R_Au_Cu(end)/max(aux.R_Au(end),1e-30));
fprintf('============================================================\n\n');
end


%% ===================================================================
%  SWEEP  -  vary ONE parameter
%  ===================================================================
function sweep(p_base, field, values, plot_key)
%SWEEP  Re-run the model for several values of one parameter.
%
%   sweep(p, 'k_cat', [0.5 2 8 32], 'Au_recovery')
%
%   field     any field name in default_params()
%   values    numeric vector, or cell array for text fields
%             e.g. sweep(p, 'gold_model', {'A','B'}, 'Au_recovery')
%   plot_key  see get_series() for the full list

if nargin < 4, plot_key = 'Au_recovery'; end
if ~iscell(values), values = num2cell(values); end

figure('Color', 'w', 'Name', sprintf('Sweep: %s', field));
hold on; grid on;
leg = cell(1, numel(values));

for i = 1:numel(values)
    p = p_base;
    p.(field) = values{i};              % <-- the one thing that changes

    [t, Y, aux] = run_model(p);         % run_model calls refresh() internally
    plot(t/60, get_series(Y, aux, plot_key), 'LineWidth', 1.6);

    if ischar(values{i})
        leg{i} = sprintf('%s = %s', field, values{i});
    else
        leg{i} = sprintf('%s = %g', field, values{i});
    end
end

xlabel('time (h)');
ylabel(label_for(plot_key));
title(sprintf('Effect of %s on %s', ...
      strrep(field,'_','\_'), strrep(plot_key,'_','\_')));
legend(leg, 'Location', 'best', 'Interpreter', 'none');
% NOTE: axes are left to autoscale. Forcing ylim([0 100]) on recovery makes a
% realistic few-percent result look like a flat line on the x-axis.
hold off;
end


%% ===================================================================
%  SWEEP2  -  vary TWO parameters, plot the end-point as a surface
%  ===================================================================
function sweep2(p_base, f1, v1, f2, v2, plot_key)
%SWEEP2  End-of-run value of plot_key over a grid of two parameters.
%
%   sweep2(p, 'F_in', [5 20 80], 'k_cat', [1 4 16], 'Au_recovery')

if nargin < 6, plot_key = 'Au_recovery'; end

Z = zeros(numel(v2), numel(v1));
for i = 1:numel(v1)
    for j = 1:numel(v2)
        p = p_base;
        p.(f1) = v1(i);
        p.(f2) = v2(j);
        [~, Y, aux] = run_model(p);
        s = get_series(Y, aux, plot_key);
        Z(j,i) = s(end);
    end
end

figure('Color', 'w', 'Name', sprintf('Sweep2: %s vs %s', f1, f2));
imagesc(1:numel(v1), 1:numel(v2), Z);
set(gca, 'YDir', 'normal', ...
    'XTick', 1:numel(v1), 'XTickLabel', compose('%g', v1), ...
    'YTick', 1:numel(v2), 'YTickLabel', compose('%g', v2));
xlabel(strrep(f1,'_','\_'));
ylabel(strrep(f2,'_','\_'));
c = colorbar; c.Label.String = sprintf('%s at t_{end}', strrep(plot_key,'_','\_'));
title(sprintf('%s at t = %.1f h', strrep(plot_key,'_','\_'), p_base.t_end/60));

% overlay the numbers
for i = 1:numel(v1)
    for j = 1:numel(v2)
        text(i, j, sprintf('%.1f', Z(j,i)), 'HorizontalAlignment','center', ...
             'Color', 'w', 'FontWeight', 'bold');
    end
end
end


%% ===================================================================
%  MODEL A  vs  MODEL B
%  ===================================================================
function compare_gold_models(p_base)

pA = p_base; pA.gold_model = 'A';  [tA, ~, aA] = run_model(pA);
pB = p_base; pB.gold_model = 'B';  [tB, ~, aB] = run_model(pB);

figure('Color', 'w', 'Name', 'Model A vs Model B');

subplot(1,2,1);
plot(tA/60, aA.Au_recovery, 'LineWidth', 1.6); hold on;
plot(tB/60, aB.Au_recovery, 'LineWidth', 1.6); grid on;
xlabel('time (h)'); ylabel('Au recovery (%)');
legend('Model A (O_2 only)', 'Model B (O_2 + Cu(II))', 'Location', 'best');
title('Gold recovery');

subplot(1,2,2);
semilogy(tA/60, max(aA.R_Au, 1e-12), 'LineWidth', 1.6); hold on;
semilogy(tB/60, max(aB.R_Au, 1e-12), 'LineWidth', 1.6); grid on;
xlabel('time (h)'); ylabel('R_{Au} (\mumol min^{-1})');
legend('Model A', 'Model B', 'Location', 'best');
title('Gold leaching rate');

if exist('sgtitle', 'file')
    sgtitle('Effect of the Cu(II) oxidant pathway', 'FontWeight', 'bold');
end

fprintf('\n--- Model comparison at t = %.1f h ---\n', p_base.t_end/60);
fprintf('  Model A:  Au %6.2f %%   Cu %6.2f %%\n', ...
        aA.Au_recovery(end), aA.Cu_recovery(end));
fprintf('  Model B:  Au %6.2f %%   Cu %6.2f %%\n\n', ...
        aB.Au_recovery(end), aB.Cu_recovery(end));
end