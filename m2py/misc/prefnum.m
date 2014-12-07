function [PfA,PfS,EdS,HsA,HsI] = prefnum(InA,PfT,varargin)
% Round numeric vector to nearest preferred number/value, using inbuilt/custom number series.
%
% (c) 2012 Stephen Cobeldick
%
% ### Function ###
%
% Round the elements of a horizontal numeric vector to values chosen
% from a Preferred Number Series (PNS). The PNS may be one of:
% - Standard PNS (1-2-5, Renard and electronic IEC 60063 are inbuilt)
% - Custom PNS numeric vector (repeating every decade)
% - Custom PNS function (handle of a continuous function in one variable)
%
% Syntax:
%  PfA = prefnum(InA,PfTok)     % Select an inbuilt PNS (see tables below).
%  PfA = prefnum(InA,PfVec)     % Use a custom PNS numeric vector (fast).
%  PfA = prefnum(InA,PfFun)     % Use a custom PNS function (slow).
%  [PfA,PfSet,EdgeSet,HistCnt] = prefnum(...) % PNS range, edges and bin count.
%
% If using an inbuilt PNS:
%  - InA zero-value elements are returned as zero in PfA.
%  - InA element values must be finite, real and positive.
%
% If using a custom numeric vector PNS:
%  - InA zero-value elements are returned as zero in PfA.
%  - InA element values must be finite, real and positive.
%  - The PNS vector element values must be over one decade only,
%    monotonic increasing, finite, real and positive.
%
% If using a custom PNS function handle:
%  - The PNS function f(X) must be monotonic increasing with X.
%  - Returns f(X) that are best matches to the InA values, for integer X values.
%  - InA element values must be finite and real.
%  - Solution is found using MATLAB's "fzero", the optional inputs may be passed as well.
%  - An error 'No solution found for given preferred number series...' means
%    that the given function and element value does not have a real solution.
%
% If the whole PNS domain can be calculated, then use "hist"/"histc" directly.
%
% See also ROUND HISTC HIST LOG10 FZERO
%
% ### Examples ###
%
% prefnum([514,7.6,37,0.9],'E6')    % Electronic, six steps per decade.
%   ans = [470,6.8,33,1]
%
% prefnum([514,7.6,37,0.9],'E12')   % Electronic, twelve steps per decade.
%   ans = [560,8.2,39,0.82]
%
% prefnum([514,7.6,37,0.9],'R10')   % Renard, ten steps per decade.
%   ans = [500,8.0,40,1]
%
% prefnum([514,7.6,37,0.9],'R"5')   % Renard, five steps per decade, twice rounded.
%   ans = [600,6.0,40,1]
%
% prefnum([514,7.6,37,0.9],'125')   % 1-2-5, three steps per decade.
%   ans = [500,10,50,1]
%
% prefnum([514,7.6,37,0.9],[25,75]) % Custom vector, two steps per decade.
%   ans = [750,7.5,25,0.75]
%
% prefnum([514,7.6,37,0.9],1)       % Custom vector, nearest order of magnitude.
%   ans = [100,10,10,1]
%
% prefnum([514,7.6,37,0.9],@(x)2^x) % Custom function handle, nearest binary / power of two.
%   ans = [512,8,32,1]
%
% [A,P,E] = prefnum(-11:11,@(x)3*x) % Custom function handle, nearest multiple of three.
%  A = [-12,-9,-9,-9,-6,-6,-6,-3,-3,-3,0,0,0,3,3,3,6,6,6,9,9,9,12]
%  P = [-12,-9,-6,-3,0,3,6,9,12]
%  E = [-13.5,-10.5,-7.5,-4.5,-1.5,1.5,4.5,7.5,10.5,13.5]
%
% [A,P] = prefnum([5,300],'E12')    % Electronic, nearest E12 values from 5 to 300.
%  A = [4.7,330]
%  P = [4.7,5.6,6.8,8.2,10,12,15,18,22,27,33,39,47,56,68,82,100,120,150,180,220,270,330]
%
% [~,~,E,H] = prefnum(1:149,'125',0)% Draw a histogram with a bin width
% bar(H)                            % that increases as a ~geometric series.
% L = arrayfun(@num2str,E,'UniformOutput',false)
% set(gca,'XTickLabel',strcat(L(1:end-1),'<',L(2:end)))
%
% ### Inbuilt PNS Tokens ###
%
% # 1-2-5
%
%  PNS token: '125' (three steps per decade).
%  Tolerance default = 0.36, giving minimum tolerance overlap/separation.
%
% # Electronic (IEC 60063) (resistors, capacitors, inductors, zener diodes...)
%
%  PNS token:        | E6  | E12 | E24  | E48  | E96  | E192  |
%  ------------------|-----|-----|------|------|------|-------|
%  Tolerance default | 0.2 | 0.1 | 0.05 | 0.02 | 0.01 | 0.005 |
%
% # Renard (defined to three significant digits) (tolerance default = zero)
%
%  PNS token: Basic | R5  | R10  | R20  | R40  | R80 |
%  -----------------|-----|------|------|------|-----|
%   "       Rounded | R'5 | R'10 | R'20 | R'40 |     |
%  -----------------|-----|------|------|------|-----|
%   " Twice Rounded | R"5 | R"10 | R"20 |      |     |
%
% ### Rounding and Tolerance ###
%
% If using an inbuilt PNS or a custom numeric vector PNS:
%  The tolerance defines the rounding edges (selection boundaries), between
%  which the input vector elements round to the best matching PNS value.
%  The selection edges (see "histc") are generated from the PNS values and
%  the PNS tolerance: edge_2 = average of (1+Tol)*PNS_1 and (1-Tol)*PNS_2.
%
%          | Edges halfway between  | Examples:          (PNS = [20,30,60])
%  --------|------------------------|--------------------------------------
%  Tol = 0 | PNS values             | [..,25,45,130,..]             (Tol=0)
%  --------|------------------------|--------------------------------------
%  Tol > 0 | tolerance limit values | [..,23.25,41.25,112.5,..]  (Tol=0.25)
%
%  The tolerance may be set using the optional third argument.
%
% If using a custom PNS function handle:
%  The edges are function values at the midpoints between the PNS range values.
%  Example: fn = @(x)2^x -> PNS = [1,2,4,..], edges = [0.7,1.41,2.82,..].
%
% ### Inputs and Outputs ###
%
% All numeric vectors are horizontal. Outputs are empty if no matches found.
%
% Outputs:
%  PfA = InA elements rounded to nearest PNS value, numel = A.
%  PfS = PNS range over all InA values (InA domain), numel = P.
%  EdS = Edge values corresponding to PNS vector PfS, numel = P+1.
%  HsA = Number of elements matching each PNS element, numel = P.
%  HsI = Index of HsA, such that HsA(k) = sum(HsI==k), numel = A.
% Inputs:
%  InA = Numeric vector, finite and real element values, numel = A.
%  PfT = String, as per tables above, to select an inbuilt PNS.
%      = Numeric vector, values are finite, positive, monotonic increasing and of
%        the same order of magnitude to define a PNS that repeats every decade.
%      = Function handle, a monotonic increasing function in one variable.
% If using an inbuilt PNS or a custom numeric vector PNS:
%  In1 = Numeric scalar, *optional decimal tolerance value (eg 0.2 = 20%),
%        for a custom PNS vector the tolerance default = zero.
% If using a custom PNS function handle:
%  In1 = Numeric scalar, *optional seed for MATLAB's "fzero", default = zero.
%  In2 = Struct, *optional settings structure for MATLAB's "fzero" function.
%
% Outputs = [PfA,PfS,EdS,HsA]
% Inputs = (InA,PfT,In1*,In2*)

% Non-zero value InA location indices:
IxZ = InA>0;
IsV = true;
%
% Define PNS:
if isempty(InA)
    [PfA,PfS,EdS,HsA,HsI] = deal([]);
    return
elseif strncmp('E',PfT,1) % electronic
    [PfT,PfO,DfA] = PrNmELkUp(PfT);
elseif strncmp('R',PfT,1) % Renard
    [PfT,PfO,DfA] = PrNmRLkUp(PfT);
elseif strcmp('125',PfT)  % 1-2-5
    DfA = {0.36};
    PfO = 0;
    PfT = [1,2,5];
elseif ~isempty(PfT) && isnumeric(PfT)
    % Custom: Numeric Vector (over one magnitude)
    DfA = {0};
    %
    % Order of magnitude of PNS:
    PfO = floor(log10([min(PfT),max(PfT)]));
    %
    if PfO(1)~=PfO(2)
        error('Custom preferred number series must cover one order of magnitude only.')
    end
    %
    PfO = PfO(1);
elseif isa(PfT,'function_handle')
    % Custom: Function Handle
    IsV = false;
    IxZ = true(size(InA));
    %
    DfA = {0,struct('Display','notify','TolX',eps,'FunValCheck','on','OutputFcn',[],'PlotFcns',[])};
    DfA(1:numel(varargin)) = varargin;
    %
    % Find min and max of PNS range:
    VlN = floor(fzero(@(x)PfT(x)-min(InA),DfA{1},DfA{2}));
    VlX = ceil(fzero(@(x)PfT(x)-max(InA),DfA{1},DfA{2}));
    %
    % Domain of PNS (wider than InA values):
    PfP = VlN-1:1+VlX;
    PfS = arrayfun(PfT,PfP);
    % Edges of the domain (ie between the PNS values):
    EdS = arrayfun(PfT,(PfP(1:end-1)+PfP(2:end))/2);
else
    error('Unrecognized preferred number series.')
end
%
if IsV % Vector defined PNS
    DfA(1:numel(varargin)) = varargin;
    Tol = DfA{1};
    %
    % Order of magnitude of InA max and min:
    PfN = floor(log10(min(InA(IxZ))));
    PfX = floor(log10(max(InA(IxZ))));
    %
    % Domain of PNS (wider than InA values):
    switch numel(PfT)
        case 1
            PfP = PfN-2:2+PfX;
            PfS = (PfT*10.^PfP)/10^PfO;
        case 2
            PfP = PfN-1:1+PfX;
            PfS = PfT'*10.^PfP;
            PfS = PfS(:)'/10^PfO;
        otherwise
            PfP = PfN:PfX;
            PfS = PfT'*10.^PfP;
            PfS = [PfT(end-1:end).*10^(PfN-1),PfS(:)',PfT(1:2).*10^(PfX+1)]/10^PfO;
    end
    %
    % Edges between the PNS values:
    EdS = ((1+Tol(1))*PfS(1:end-1)+(1-Tol(end))*PfS(2:end))/2;
end
%
if numel(EdS)<2
    [PfA,PfS,EdS,HsA,HsI] = deal([]);
    return
end
%
% Range of the required PNS values (exactly covering InA):
[HsA,HsI] = histc(InA(IxZ),EdS);
% Remove PNS domain and edge values outside of this range:
bg = min(HsI);
en = max(HsI);
HsI = HsI-bg+1;
HsA = HsA(bg:en);
EdS = EdS(bg:en+1);
PfS = PfS(bg+1:en+1);
%
% Output the rounded values:
PfA(IxZ) = PfS(HsI);
%
% Zero-values inserted into output arrays:
if ~all(IxZ)
    PfA(~IxZ) = 0;
    HsI(IxZ) = HsI;
    HsI(~IxZ) = 0;
    HsI = HsI+1;
    HsA = [sum(~IxZ),HsA];
    EdS = [0,EdS];
    PfS = [0,PfS];
end
%
end
%--------------------------------------------------------------------------
function [PfT,PfO,DfA] = PrNmELkUp(PfT)
% Electronic (IEC 60063) PNS, to three significant digits.
%
PfO = 2;
%
switch PfT
    case 'E6'
        DfA = {0.2};
        PfT = [100,150,220,330,470,680];
    case 'E12'
        DfA = {0.1};
        PfT = [100,120,150,180,220,270,330,390,470,560,680,820];
    case 'E24'
        DfA = {0.05};
        PfT = [100,110,120,130,150,160,180,200,220,240,270,300,330,360,390,430,470,510,560,620,680,750,820,910];
    case 'E48'
        DfA = {0.02};
        PfT = [100,105,110,115,121,127,133,140,147,154,162,169,178,187,196,205,215,226,237,249,261,274,287,301,...
               316,332,348,365,383,402,422,442,464,487,511,536,562,590,619,649,681,715,750,787,825,866,909,953];
    case 'E96'
        DfA = {0.01};
        PfT = [100,102,105,107,110,113,115,118,121,124,127,130,133,137,140,143,147,150,154,158,162,165,169,174,...
               178,182,187,191,196,200,205,210,215,221,226,232,237,243,249,255,261,267,274,280,287,294,301,309,...
               316,324,332,340,348,357,365,374,383,392,402,412,422,432,442,453,464,475,487,499,511,523,536,549,...
               562,576,590,604,619,634,649,665,681,698,715,732,750,768,787,806,825,845,866,887,909,931,953,976];
    case 'E192'
        DfA = {0.005};
        PfT = [100,101,102,104,105,106,107,109,110,111,113,114,115,117,118,120,121,123,124,126,127,129,130,132,...
               133,135,137,138,140,142,143,145,147,149,150,152,154,156,158,160,162,164,165,167,169,172,174,176,...
               178,180,182,184,187,189,191,193,196,198,200,203,205,208,210,213,215,218,221,223,226,229,232,234,...
               237,240,243,246,249,252,255,258,261,264,267,271,274,277,280,284,287,291,294,298,301,305,309,312,...
               316,320,324,328,332,336,340,344,348,352,357,361,365,370,374,379,383,388,392,397,402,407,412,417,...
               422,427,432,437,442,448,453,459,464,470,475,481,487,493,499,505,511,517,523,530,536,542,549,556,...
               562,569,576,583,590,597,604,612,619,626,634,642,649,657,665,673,681,690,698,706,715,723,732,741,...
               750,759,768,777,787,796,806,816,825,835,845,856,866,876,887,898,909,920,931,942,953,965,976,988];
    otherwise
        error('Unrecognized preferred number series token.')
end
%
end
%--------------------------------------------------------------------------
function [PfT,PfO,DfA] = PrNmRLkUp(PfT)
% Renard PNS, to three significant digits.
%
PfO = 2;
DfA = {0};
%
switch PfT
    case 'R5'
        PfT = [100,158,251,398,631];
    case 'R10'
        PfT = [100,125,160,200,250,315,400,500,630,800];
    case 'R20'
        PfT = [100,112,125,140,160,180,200,224,250,280,315,355,400,450,500,560,630,710,800,900];
    case 'R40'
        PfT = [100,106,112,118,125,132,140,150,160,170,180,190,200,212,224,236,250,265,280,300,...
               315,335,355,375,400,425,450,475,500,530,560,600,630,670,710,750,800,850,900,950];
    case 'R80'
        PfT = [100,103,106,109,112,115,118,122,125,128,132,136,140,145,150,155,160,165,170,175,...
               180,185,190,195,200,206,212,218,224,230,236,243,250,258,265,272,280,290,300,307,...
               315,325,335,345,355,365,375,387,400,412,425,437,450,462,475,487,500,515,530,545,...
               560,580,600,615,630,650,670,690,710,730,750,775,800,825,850,875,900,925,950,975];
    case 'R''5'
        PfT = [100,160,250,400,630];
    case 'R''10'
        PfT = [100,125,160,200,250,320,400,500,630,800];
    case 'R''20'
        PfT = [100,110,125,140,160,180,200,220,250,280,320,360,400,450,500,560,630,710,800,900];
    case 'R''40'
        PfT = [100,105,110,120,125,130,140,150,160,170,180,190,200,210,220,240,250,260,280,300,...
               320,340,360,380,400,420,450,480,500,530,560,600,630,670,710,750,800,850,900,950];
    case 'R"5'
        PfT = [100,150,250,400,600];
    case 'R"10'
        PfT = [100,120,150,200,250,300,400,500,600,800];
    case 'R"20'
        PfT = [100,110,120,140,150,180,200,220,250,280,300,350,400,450,500,550,600,700,800,900];
    otherwise
        error('Unrecognized preferred number series token.')
end
%
end
%-----------------------------------------------------------------------End
