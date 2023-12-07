import re
class B:
	def __init__(A):A.table={}
	def add(C,*A):
		if len(A)<3:raise TypeError('Require >2 arguments.')
		B={}
		if isinstance(A[-1],dict):B.update(A[-1]);A=A[:-1]
		B['type']=A[-1];B['value']=A[-2];D=A[:-2]
		for E in D:C.table[E]=B.copy()
	def build(A):return A.table.copy()
_AA='varepsilon'
_A9='overbrace'
_A8='underbrace'
_A7='underline'
_A6='Leftrightarrow'
_A5='Leftarrow'
_A4='Rightarrow'
_A3='leftrightarrow'
_A2='leftarrow'
_A1='twoheadrightarrowtail'
_A0='twoheadrightarrow'
_z='rightarrowtail'
_y='rightarrow'
_x='downarrow'
_w='uparrow'
_v='arctan'
_u='arccos'
_t='arcsin'
_s='rceiling'
_r='lceiling'
_q='rfloor'
_p='lfloor'
_o='square'
_n='diamond'
_m='triangle'
_l='because'
_k='therefore'
_j='emptyset'
_i='partial'
_h='rangle'
_g='langle'
_f='models'
_e='exists'
_d='forall'
_c='implies'
_b='propto'
_a='approx'
_Z='supseteq'
_Y='subseteq'
_X='supset'
_W='subset'
_V='succeq'
_U='preceq'
_T='bigcup'
_S='bigcap'
_R='bigvee'
_Q='bigwedge'
_P='otimes'
_O='bowtie'
_N='rtimes'
_M='ltimes'
_L='setminus'
_K='backslash'
_J='infix'
_I='frac'
_H='abs'
_G='vbar'
_F='binary'
_E='rparen'
_D='lparen'
_DE='lrparen'
_C='unary'
_B='unaryfunc'
_A='symbol'
T=B()
T.add('+','plus',_A)
T.add('-','minus',_A)
T.add('*','cdot','cdot',_A)
T.add('**','ast','ast',_A)
T.add('***','star','star',_A)
T.add('//','slash',_A)
T.add('\\\\',_K,_K,_A)
T.add(_L,_L,_A)
T.add('xx','times','times',_A)
T.add('|><',_M,_M,_A)
T.add('><|',_N,_N,_A)
T.add('|><|',_O,_O,_A)
T.add('-:','div','divide','div',_A)
T.add('@','circ','circ',_A)
T.add('o+','oplus','oplus',_A)
T.add('ox',_P,_P,_A)
T.add('o.','odot','odot',_A)
T.add('sum','sum',_A)
T.add('prod','prod',_A)
T.add('^^','wedge','wedge',_A)
T.add('^^^',_Q,_Q,_A)
T.add('vv','vee','vee',_A)
T.add('vvv',_R,_R,_A)
T.add('nn','cap','cap',_A)
T.add('nnn',_S,_S,_A)
T.add('uu','cup','cup',_A)
T.add('uuu',_T,_T,_A)
T.add('=','eq',_A)
T.add('!=','ne','ne',_A)
T.add(':=','assign',_A)
T.add('<','lt','lt',_A)
T.add('mlt','ll','mlt',_A)
T.add('>','gt','gt',_A)
T.add('mgt','gg','mgt',_A)
T.add('<=','le','le',_A)
T.add('>=','ge','ge',_A)
T.add('-<','-lt','prec','prec',_A)
T.add('>-','succ','succ',_A)
T.add('-<=',_U,_U,_A)
T.add('>-=',_V,_V,_A)
T.add('in','in',_A)
T.add('!in','notin','notin',_A)
T.add('sub',_W,_W,_A)
T.add('sup',_X,_X,_A)
T.add('sube',_Y,_Y,_A)
T.add('supe',_Z,_Z,_A)
T.add('-=','equiv','equiv',_A)
T.add('~','sim','sim',_A)
T.add('~=','cong','cong',_A)
T.add('~~',_a,_a,_A)
T.add('prop',_b,_b,_A)
T.add('and','and',_A)
T.add('or','or',_A)
T.add('not','neg','not',_A)
T.add('=>',_c,_c,_A)
T.add('if','if',_A)
T.add('<=>','iff','iff',_A)
T.add('AA',_d,_d,_A)
T.add('EE',_e,_e,_A)
T.add('_|_','bot','bot',_A)
T.add('TT','top','top',_A)
T.add('|--','vdash','vdash',_A)
T.add('|==',_f,_f,_A)
T.add('(','left(',_D,_D)
T.add(')','right)',_E,_E)
T.add('[','left[','lbracket',_D)
T.add(']','right]','rbracket',_E)
T.add('{','lbrace',_D)
T.add('}','rbrace',_E)
T.add('(:','<<',_g,_g,_D)
T.add(':)','>>',_h,_h,_E)
T.add('{:',None,_D)
T.add(':}',None,_E)
T.add(':|:',_G,_A)
T.add('|:',_G,_D)
T.add(':|',_G,_E)
T.add('|',_G,_DE)
T.add('int','integral',_A)
T.add('dx','dx',_A)
T.add('dy','dy',_A)
T.add('dz','dz',_A)
T.add('dt','dt',_A)
T.add('oint','contourintegral',_A)
T.add('del',_i,_i,_A)
T.add('grad','nabla','nabla',_A)
T.add('+-','pm','pm',_A)
T.add('-+','mp','mp',_A)
T.add('O/',_j,_j,_A)
T.add('oo','infty','infty',_A)
T.add('aleph','aleph',_A)
T.add('...','ldots','ellipsis',_A)
T.add(':.',_k,_k,_A)
T.add(":'",_l,_l,_A)
T.add('/_','angle','angle',_A)
T.add('/_\\',_m,_m,_A)
T.add("'",'prime','prime',_A)
T.add('tilde','tilde',_C)
T.add('\\ ','nbsp',_A)
T.add('frown','frown',_A)
T.add('quad','quad',_A)
T.add('qquad','qquad',_A)
T.add('cdots','cdots',_A)
T.add('vdots','vdots',_A)
T.add('ddots','ddots',_A)
T.add(_n,_n,_A)
T.add(_o,_o,_A)
T.add('|__',_p,_p,_A)
T.add('__|',_q,_q,_A)
T.add('|~',_r,_r,_A)
T.add('~|',_s,_s,_A)
T.add('CC','dstruck_captial_c',_A)
T.add('NN','dstruck_captial_n',_A)
T.add('QQ','dstruck_captial_q',_A)
T.add('RR','dstruck_captial_r',_A)
T.add('ZZ','dstruck_captial_z',_A)
T.add('f','f',_B)
T.add('g','g',_B)
T.add('sin','sin',_B)
T.add('Sin','Sin',_B)
T.add('cos','cos',_B)
T.add('Cos','Cos',_B)
T.add('tan','tan',_B)
T.add('Tan','Tan',_B)
T.add('sinh','sinh',_B)
T.add('Sinh','Sinh',_B)
T.add('cosh','cosh',_B)
T.add('Cosh','Cosh',_B)
T.add('tanh','tanh',_B)
T.add('Tanh','Tanh',_B)
T.add('cot','cot',_B)
T.add('Cot','Cot',_B)
T.add('sec','sec',_B)
T.add('Sec','Sec',_B)
T.add('csc','csc',_B)
T.add('Csc','Csc',_B)
T.add(_t,_t,_B)
T.add(_u,_u,_B)
T.add(_v,_v,_B)
T.add('coth','coth',_B)
T.add('sech','sech',_B)
T.add('csch','csch',_B)
T.add('exp','exp',_B)
T.add(_H,_H,_B)
T.add('Abs',_H,_B)
T.add('norm','norm',_B)
T.add('floor','floor',_B)
T.add('ceil','ceil',_B)
T.add('log','log',_B)
T.add('Log','Log',_B)
T.add('ln','ln',_B)
T.add('Ln','Ln',_B)
T.add('det','det',_B)
T.add('gcd','gcd',_B)
T.add('lcm','lcm',_B)
T.add('dim','dim',_A)
T.add('ker','ker',_A)
T.add('mod','mod',_A)
T.add('lub','lub',_A)
T.add('glb','glb',_A)
T.add('lim','lim',_A)
T.add('Lim','Lim',_A)
T.add('min','min',_A)
T.add('max','max',_A)
T.add('uarr',_w,_w,_A)
T.add('darr',_x,_x,_A)
T.add('rarr',_y,_y,_A)
T.add('->','to','to',_A)
T.add('>->',_z,_z,_A)
T.add('->>',_A0,_A0,_A)
T.add('>->>',_A1,_A1,_A)
T.add('|->','mapsto','mapsto',_A)
T.add('larr',_A2,_A2,_A)
T.add('harr',_A3,_A3,_A)
T.add('rArr',_A4,_A4,_A)
T.add('lArr',_A5,_A5,_A)
T.add('hArr',_A6,_A6,_A)
T.add('sqrt','sqrt',_C)
T.add('root','root',_F)
T.add(_I,_I,_F)
T.add('/',_I,_J)
T.add('stackrel','stackrel',_F)
T.add('overset','overset',_F)
T.add('underset','underset',_F)
T.add('_','sub',_J)
T.add('^','sup',_J)
T.add('hat','hat',_C)
T.add('bar','overline',_C)
T.add('vec','vec',_C)
T.add('dot','dot',_C)
T.add('ddot','ddot',_C)
T.add('overarc','overparen','overarc',_C)
T.add('ul',_A7,_A7,_C)
T.add('ubrace',_A8,_A8,_C)
T.add('obrace',_A9,_A9,_C)
T.add('cancel','cancel',_C)
T.add('bb','mathbf','bold',_C)
T.add('bbb','mathbb','double_struck',_C)
T.add('cc','mathcal','script',_C)
T.add('tt','mathtt','monospace',_C)
T.add('fr','mathfrak','fraktur',_C)
T.add('sf','mathsf','sans_serif',_C)
T.add('alpha','alpha',_A)
T.add('Alpha','Alpha',_A)
T.add('beta','beta',_A)
T.add('Beta','Beta',_A)
T.add('gamma','gamma',_A)
T.add('Gamma','Gamma',_A)
T.add('delta','delta',_A)
T.add('Delta','Delta',_A)
T.add('epsi','epsilon','epsilon',_A)
T.add('Epsilon','Epsilon',_A)
T.add(_AA,_AA,_A)
T.add('zeta','zeta',_A)
T.add('Zeta','Zeta',_A)
T.add('eta','eta',_A)
T.add('Eta','Eta',_A)
T.add('theta','theta',_A)
T.add('Theta','Theta',_A)
T.add('vartheta','vartheta',_A)
T.add('iota','iota',_A)
T.add('Iota','Iota',_A)
T.add('kappa','kappa',_A)
T.add('Kappa','Kappa',_A)
T.add('lambda','lambda',_A)
T.add('Lambda','Lambda',_A)
T.add('mu','mu',_A)
T.add('Mu','Mu',_A)
T.add('nu','nu',_A)
T.add('Nu','Nu',_A)
T.add('xi','xi',_A)
T.add('Xi','Xi',_A)
T.add('omicron','omicron',_A)
T.add('Omicron','Omicron',_A)
T.add('pi','pi',_A)
T.add('Pi','Pi',_A)
T.add('rho','rho',_A)
T.add('Rho','Rho',_A)
T.add('sigma','sigma',_A)
T.add('Sigma','Sigma',_A)
T.add('tau','tau',_A)
T.add('Tau','Tau',_A)
T.add('upsilon','upsilon',_A)
T.add('Upsilon','Upsilon',_A)
T.add('phi','phi',_A)
T.add('Phi','Phi',_A)
T.add('varphi','varphi',_A)
T.add('chi','chi',_A)
T.add('Chi','Chi',_A)
T.add('psi','psi',_A)
T.add('Psi','Psi',_A)
T.add('omega','omega',_A)
T.add('Omega','Omega',_A)
SYMS=T.build()
s_l_m_l=max(len(key)for key in SYMS)
class Tzr:
	WS='\\s+';NBR='[0-9]+(?:\\.[0-9]+)?';Q_TXT='"[^"]*"';T_TXT='text\\([^)]*\\)';SYM=f"((?:\\\\[\\s0-9]|[^\\s0-9]){{1,{s_l_m_l}}})"
	def __init__(A,expr):A.expr=expr;A.cur_i=0;A.p_b_t=None
	def s_c_i(A):return A.cur_i,A.expr,A.p_b_t
	def r_s_i(A, ss):
		if ss is not None:A.cur_i=ss[0];A.expr=ss[1];A.p_b_t=ss[2];ss=None
	def n_t(A):
		if A.p_b_t:C=A.p_b_t;A.p_b_t=None;return C
		A.s_w()
		if A.cur_i>=len(A.expr):return{'value':None,'type':'eof'}
		B=A.p(1)
		if B=='"':return A.r_q_t()
		if B=='t'and A.p(5)=='text(':return A.r_t_t()
		if B in'-0123456789':return A.r_n()or A.r_s()
		return A.r_s()
	def p_b(B,token):
		A=token
		if A['type']!='eof':B.p_b_t=A
	def rep_m(D,string,pattern,replacement):
		A=string;B=re.match(pattern,A)
		if B:C=B.end();return replacement+A[C:]
		else:return A
	def s_w(A):A.expr=A.rep_m(A.expr[A.cur_i:],Tzr.WS,'');A.cur_i=0
	def p(A,length):return A.expr[A.cur_i:A.cur_i+length]
	def r_q_t(A):return A.r_val(Tzr.Q_TXT,lambda match:{'value':match[1:-1],'type':'text'})
	def r_t_t(A):return A.r_val(Tzr.T_TXT,lambda match:{'value':match[5:-1],'type':'text'})
	def r_n(A):return A.r_val(Tzr.NBR,lambda match:{'value':match,'type':'number'})
	def r_val(A,regex,callback):
		B=re.match(regex,A.expr[A.cur_i:])
		if B:A.cur_i+=len(B[0]);return callback(B[0])
	def p_a_f_s(A):return re.match(Tzr.SYM,A.expr[A.cur_i:])
	def r_s(B):
		C=B.p_a_f_s()
		if C:
			A=C[0]
			while len(A)>1 and A not in SYMS:A=A[:-1]
			B.cur_i+=len(A)
			if A in SYMS:return{**SYMS[A],'text':A}
			return{'value':A,'type':'identifier'}
class Node:
	def __init__(A):A._parent=None;A._children=[];A._index=-1
	@property
	def parent(self):return self._parent
	@parent.setter
	def parent(self,parent):self._parent=parent
	@property
	def children(self):return self._children
	@property
	def length(self):return len(self.children)
	def add(B,node):
		A=node
		if A.parent:A.parent.remove(A)
		A.parent=B;B.children.append(A)
	def remove(A,node):
		B=A.children.index(node)
		if B!=-1:del A.children[B]
		node.parent=None
	def __iter__(A):return A
	def __next__(A):
		A._index+=1
		if A._index<len(A.children):return A.children[A._index]
		A._index=-1;raise StopIteration
class Sequence(Node):
	def __init__(A,nodes):
		super().__init__()
		for B in nodes:A.add(B)
	def to_string(A):return''.join([str(A)for A in A.children])
	def __str__(A):return A.to_string()
	def __eq__(A,other):B=other;return isinstance(B,type(A))and B.length==A.length and all(C==B.children[A]for(A,C)in enumerate(A.children))
class Paren(Node):
	def __init__(A,lparen_node,expr_node,rparen_node):super().__init__();A.add(lparen_node or Empty());A.add(expr_node or Empty());A.add(rparen_node or Empty())
	@property
	def lparen(self):return self.children[0]
	@property
	def expression(self):return self.children[1]
	@property
	def rparen(self):return self.children[2]
	def to_string(A):return(str(A.lparen)if type(A.lparen)!=Empty else'')+(str(A.expression)if type(A.expression)!=Empty else'')+(str(A.rparen)if type(A.rparen)!=Empty else'')
	def __str__(A):return A.to_string()
	def __eq__(A,other):B=other;return isinstance(B,type(A))and B.lparen==A.lparen and B.expression==A.expression and B.rparen==A.rparen
class Group(Paren):0
class SubSup(Node):
	def __init__(A,base_n,sub_n,sup_n):super().__init__();A.add(base_n);A.add(sub_n or Empty());A.add(sup_n or Empty())
	@property
	def base(self):return self.children[0]
	@property
	def sub(self):
		A=self.children[1]
		if isinstance(A,Empty):return
		return A
	@property
	def sup(self):
		A=self.children[2]
		if isinstance(A,Empty):return
		return A
	def to_string(B):
		A=B.base;C=B.sub
		if C:A=f"{A}_{C}"
		D=B.sup
		if D:A=f"{A}^{D}"
		return A
	def __str__(A):return A.to_string()
	def __eq__(A,other):B=other;return isinstance(B,type(A))and B.base==A.base and B.sub==A.sub and B.sup==A.sup
class Sub(SubSup):
	def __init__(A,base_n,sub_n):super().__init__(base_n,sub_n,None)
class Sup(SubSup):
	def __init__(A,base_n,sup_n):super().__init__(base_n,None,sup_n)
class Unary(Node):
	def __init__(A,operator_n,operand_n):super().__init__();A.add(operator_n);A.add(operand_n)
	@property
	def operator(self):return self.children[0]
	@property
	def operand(self):return self.children[1]
	def to_string(A):return f"{A.operator} {A.operand}"
	def __str__(A):return A.to_string()
	def __eq__(A,other):B=other;return isinstance(B,type(A))and B.operator==A.operator and B.operand==A.operand
class UnaryFunc(Unary):
	def __init__(A,operator_n,operand_n):super().__init__(operator_n,operand_n)
	def to_string(A):
		if len(str(A.operator))==1:return f"{A.operator}{A.operand}"
		return f"{A.operator} {A.operand}"
	def __str__(A):return A.to_string()
class Binary(Node):
	def __init__(A,operator,operand1_n,operand2_n):super().__init__();A.add(operator);A.add(operand1_n);A.add(operand2_n)
	@property
	def operator(self):return self.children[0]
	@property
	def operand1(self):return self.children[1]
	@property
	def operand2(self):return self.children[2]
	def to_string(A):return f"{A.operator} {A.operand1} {A.operand2}"
	def __str__(A):return A.to_string()
	def __eq__(A,other):B=other;return isinstance(B,type(A))and B.operator==A.operator and B.operand1==A.operand1 and B.operand2==A.operand2
class BinaryInfix(Binary):
	def to_string(A):return f"{str(A.operand1)} {str(A.operator)} {str(A.operand2)}"
	def __str__(A):return A.to_string()
class Literal(Node):
	def __init__(A,value):super().__init__();A._value=value
	@property
	def value(self):return self._value
	def to_string(A):return A.value
	def __str__(A):return A.to_string()
	def __eq__(A,other):B=other;return type(B)==type(A)and B.value==A.value
class TextValue(Literal):0
class NumberValue(Literal):0
class Symbol(Literal):
	def __init__(A,value,text,type):super().__init__(value);A._text=text;A._type=type
	@property
	def text(self):return self._text
	@property
	def type(self):return self._type
	def to_string(A):return A.text
	def __str__(A):return A.to_string()
	def __eq__(B,other):A=other;return isinstance(A,type(B))and super().__eq__(A)and A.text==B.text and A.type==B.type
class Identifier(Literal):0
class Empty(Node):
	def to_string(A):return''
	def __str__(A):return A.to_string()
	def __eq__(A,other):return isinstance(other,type(A))
e_n_c=[Sequence,Paren,Group,SubSup,Sub,Sup,Unary,UnaryFunc,Binary,BinaryInfix,Literal,TextValue,NumberValue,Symbol,Identifier,Empty]
for A in e_n_c:A.name=A.__name__
class Asciimath:
	def __init__(A):A._ds={OO00OOOOOO0O000OO.__name__:OO00OOOOOO0O000OO for OO00OOOOOO0O000OO in e_n_c}
	def parse(A,input):return A._p_e(Tzr(input))
	def set(A,exd):
		for O000OOOOO0O0O000O in exd:
			for O0OO00OO00OOOOOO0 in A._ds:
				if O000OOOOO0O0O000O.name and A._ds[O0OO00OO00OOOOOO0].name==O000OOOOO0O0O000O.name:A._ds.update({O0OO00OO00OOOOOO0:O000OOOOO0O0O000O});break
	def _g_n(A,cls):return A._ds[cls.__name__]
	def _p_e(A,tzr,c_p_t=None):
		O0O0OO0OOO0OO00O0=c_p_t;O0000O000OOOOO0OO=tzr;OOO0000000000O0OO=None
		while True:
			OOO0OO0O00O0O00O0=A._p_i_e(O0000O000OOOOO0OO,O0O0OO0OOO0OO00O0);O0OO0OOOOO0O0O00O=O0000O000OOOOO0OO.n_t()
			if O0OO0OOOOO0O0O00O['type']=='infix'and O0OO0OOOOO0O0O00O['value']=='frac':
				O0OO000O0O0OOO000=A._p_i_e(O0000O000OOOOO0OO,O0O0OO0OOO0OO00O0)
				if O0OO000O0O0OOO000:OOO0000000000O0OO=A._c_e(OOO0000000000O0OO,A._g_n(BinaryInfix)(A._t_s_t(O0OO0OOOOO0O0O00O),A._u_p_n(OOO0OO0O00O0O00O0),A._u_p_n(O0OO000O0O0OOO000)))
				else:OOO0000000000O0OO=A._c_e(OOO0000000000O0OO,OOO0OO0O00O0O00O0)
			else:
				OOO0000000000O0OO=A._c_e(OOO0000000000O0OO,OOO0OO0O00O0O00O0)
				if O0OO0OOOOO0O0O00O['type']=='eof':break
				O0000O000OOOOO0OO.p_b(O0OO0OOOOO0O0O00O)
				if O0OO0OOOOO0O0O00O['type']==O0O0OO0OOO0OO00O0:break
				if O0OO0OOOOO0O0O00O["type"] == "rparen"and O0O0OO0OOO0OO00O0==_DE:break
		return OOO0000000000O0OO
	def _p_i_e(A,tzr,c_p_t):
		OOOOOO0O0OOOO0OO0=c_p_t;OOO00OO0OOO0OO000=tzr;OO00O0OOO00O000OO=A._p_s_e(OOO00OO0OOO0OO000,OOOOOO0O0OOOO0OO0);O000OO0O0O000O0OO=None;OO0OOOO000OOOO0OO=None;OO0O0O0O00OO0O0O0=OOO00OO0OOO0OO000.n_t()
		if OO0O0O0O00OO0O0O0['type']=='infix':
			if OO0O0O0O00OO0O0O0['value']=='sub':
				O000OO0O0O000O0OO=A._p_s_e(OOO00OO0OOO0OO000,OOOOOO0O0OOOO0OO0)
				if O000OO0O0O000O0OO:
					OO0O0O0O00OO0O0O0=OOO00OO0OOO0OO000.n_t()
					if OO0O0O0O00OO0O0O0['type']=='infix'and OO0O0O0O00OO0O0O0['value']=='sup':OO0OOOO000OOOO0OO=A._p_s_e(OOO00OO0OOO0OO000,OOOOOO0O0OOOO0OO0)
					else:OOO00OO0OOO0OO000.p_b(OO0O0O0O00OO0O0O0)
			elif OO0O0O0O00OO0O0O0['value']=='sup':OO0OOOO000OOOO0OO=A._p_s_e(OOO00OO0OOO0OO000,OOOOOO0O0OOOO0OO0)
			else:OOO00OO0OOO0OO000.p_b(OO0O0O0O00OO0O0O0)
		else:OOO00OO0OOO0OO000.p_b(OO0O0O0O00OO0O0O0)
		if O000OO0O0O000O0OO and OO0OOOO000OOOO0OO:return A._g_n(SubSup)(OO00O0OOO00O000OO,A._u_p_n(O000OO0O0O000O0OO),A._u_p_n(OO0OOOO000OOOO0OO))
		elif O000OO0O0O000O0OO:return A._g_n(Sub)(OO00O0OOO00O000OO,A._u_p_n(O000OO0O0O000O0OO))
		elif OO0OOOO000OOOO0OO:return A._g_n(Sup)(OO00O0OOO00O000OO,A._u_p_n(OO0OOOO000OOOO0OO))
		else:return OO00O0OOO00O000OO
	def _p_s_e(A,tzr,c_p_t):
		O0O0O000OOOO00O00=c_p_t;OOO0OO0O00O0000OO=tzr;OOOO0O0O0O000000O=OOO0OO0O00O0000OO.n_t()
		if OOOO0O0O0O000000O['type']=='lparen'or OOOO0O0O0O000000O["type"]==_DE:
			O0O0OOO0OO0O0O0O0='rparen'if OOOO0O0O0O000000O["type"]=="lparen"else _DE;OO00O000O00O00O00=OOO0OO0O00O0000OO.n_t()
			if OO00O000O00O00O00['type']==O0O0OOO0OO0O0O0O0 and OO00O000O00O00O00["type"]!=_DE:return A._g_n(Paren)(A._t_s_t(OOOO0O0O0O000000O),None,A._t_s_t(OO00O000O00O00O00))
			else:
				OOO0OO0O00O0000OO.p_b(OO00O000O00O00O00);OOO0O0OO0O000O000=A._p_e(OOO0OO0O00O0000OO,O0O0OOO0OO0O0O0O0);OO00O000O00O00O00=OOO0OO0O00O0000OO.n_t()
				if OO00O000O00O00O00['type']==O0O0OOO0OO0O0O0O0:return A._g_n(Paren)(A._t_s_t(OOOO0O0O0O000000O),OOO0O0OO0O000O000,A._t_s_t(OO00O000O00O00O00))
				else:
					OOO0OO0O00O0000OO.p_b(OO00O000O00O00O00)
					if OOOO0O0O0O000000O['type']==_DE:return A._c_e(A._t_s_t(OOOO0O0O0O000000O),OOO0O0OO0O000O000)
					else:return A._g_n(Paren)(A._t_s_t(OOOO0O0O0O000000O),OOO0O0OO0O000O000,None)
		if OOOO0O0O0O000000O['type']=='rparen':
			if O0O0O000OOOO00O00 is None:return A._t_s_t(OOOO0O0O0O000000O)
			else:OOO0OO0O00O0000OO.p_b(OOOO0O0O0O000000O);return
		elif OOOO0O0O0O000000O['type']=='unary':
			OOO0O0OO0O000O000=A._p_s_e(OOO0OO0O00O0000OO,O0O0O000OOOO00O00);OOO0O0OO0O000O000=A._u_p_n(OOO0O0OO0O000O000)
			if OOO0O0OO0O000O000 is None:OOO0O0OO0O000O000=A._g_n(Identifier)('')
			return A._g_n(Unary)(A._t_s_t(OOOO0O0O0O000000O),OOO0O0OO0O000O000)
		elif OOOO0O0O0O000000O['type']=='unaryfunc':
			s=OOO0OO0O00O0000OO.s_c_i();OOO0O0OO0O000O000=A._p_s_e(OOO0OO0O00O0000OO,O0O0O000OOOO00O00);OOO0O0OO0O000O000=A._u_p_n(OOO0O0OO0O000O000)
			if OOO0O0OO0O000O000 is None:OOO0O0OO0O000O000=A._g_n(Identifier)('')
			if len(OOOO0O0O0O000000O['value'])==1:
				if not isinstance(OOO0O0OO0O000O000,A._g_n(Paren))or not str(OOO0O0OO0O000O000.lparen).startswith('(')or isinstance(OOO0O0OO0O000O000.rparen,A._g_n(Empty)):OOO0OO0O00O0000OO.r_s_i(s);return A._t_s_t(OOOO0O0O0O000000O)
			return A._g_n(UnaryFunc)(A._t_s_t(OOOO0O0O0O000000O),OOO0O0OO0O000O000)
		elif OOOO0O0O0O000000O['type']=='binary':
			O00O0000OO0O00000=A._p_s_e(OOO0OO0O00O0000OO,O0O0O000OOOO00O00);O00O0000OO0O00000=A._u_p_n(O00O0000OO0O00000)
			if O00O0000OO0O00000 is None:O00O0000OO0O00000=A._g_n(Identifier)('')
			O000O00OOOOOO00O0=A._p_s_e(OOO0OO0O00O0000OO,O0O0O000OOOO00O00);O000O00OOOOOO00O0=A._u_p_n(O000O00OOOOOO00O0)
			if O000O00OOOOOO00O0 is None:O000O00OOOOOO00O0=A._g_n(Identifier)('')
			return A._g_n(Binary)(A._t_s_t(OOOO0O0O0O000000O),O00O0000OO0O00000,O000O00OOOOOO00O0)
		elif OOOO0O0O0O000000O['type']=='text':return A._g_n(TextValue)(OOOO0O0O0O000000O['value'])
		elif OOOO0O0O0O000000O['type']=='number':return A._g_n(NumberValue)(OOOO0O0O0O000000O['value'])
		elif OOOO0O0O0O000000O['type']=='identifier':return A._g_n(Identifier)(OOOO0O0O0O000000O['value'])
		elif OOOO0O0O0O000000O['type']=='eof':return
		else:return A._t_s_t(OOOO0O0O0O000000O)
	def _t_s_t(B,token):OOOOO0OO0OOOO0OO0=token;return B._g_n(Symbol)(OOOOO0OO0OOOO0OO0['value'],OOOOO0OO0OOOO0OO0['text'],OOOOO0OO0OOOO0OO0['type'])
	def _u_p_n(B,node):OO0O0O00O00O00O00=node;return B._g_n(Group)(OO0O0O00O00O00O00.lparen,OO0O0O00O00O00O00.expression,OO0O0O00O00O00O00.rparen)if isinstance(OO0O0O00O00O00O00,B._g_n(Paren))and(isinstance(OO0O0O00O00O00O00.lparen,B._g_n(Empty))or OO0O0O00O00O00O00.lparen.type=='lparen')and(isinstance(OO0O0O00O00O00O00.rparen,B._g_n(Empty))or OO0O0O00O00O00O00.rparen.type=='rparen')else OO0O0O00O00O00O00
	def _exp(B,*OO0OOO0O00O00O000):
		if len(OO0OOO0O00O00O000)==0:return
		elif len(OO0OOO0O00O00O000)==1:return OO0OOO0O00O00O000[0]
		else:return B._g_n(Sequence)(OO0OOO0O00O00O000)
	def _c_e(C,expr1,expr2):
		O00000OO0O0000OO0=expr1;O0OOOO0OO0OOOOO0O=expr2
		if isinstance(O00000OO0O0000OO0,C._g_n(Sequence)):
			if isinstance(O0OOOO0OO0OOOOO0O,C._g_n(Sequence)):return C._exp(*O00000OO0O0000OO0,*O0OOOO0OO0OOOOO0O)
			elif O0OOOO0OO0OOOOO0O is None:return O00000OO0O0000OO0
			else:return C._exp(*O00000OO0O0000OO0,O0OOOO0OO0OOOOO0O)
		elif O00000OO0O0000OO0 is None:return O0OOOO0OO0OOOOO0O
		elif isinstance(O0OOOO0OO0OOOOO0O,C._g_n(Sequence)):return C._exp(O00000OO0O0000OO0,*O0OOOO0OO0OOOOO0O)
		elif O0OOOO0OO0OOOOO0O is None:return O00000OO0O0000OO0
		else:return C._exp(O00000OO0O0000OO0,O0OOOO0OO0OOOOO0O)
amparser = Asciimath()
