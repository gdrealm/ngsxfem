"""
(ngs)xfem
=========

A module for unfitted discretizations in NGSolve

Modules:
xfem.lsetcuving ... isoparametric unfitted FEM
"""

from ngsolve.comp import *
from ngsolve.fem import *
from ngsolve.utils import L2
from xfem.ngsxfem_py import *
from xfem.ngsxfem_xfem_py import *
from xfem.ngsxfem_utils_py import *
from xfem.ngsxfem_cutint_py import *
from xfem.ngsxfem_lsetcurving_py import *

def extend(func):
    """
Evaluates the XFiniteElement-function independent of the level set domains.

Note:
This will lead to the same behavior as the function that the XFiniteElement-function is based
on.
    """
    if func.derivname == "extend":
        return func.Deriv()
    add = func.Operator("extend")
    if add:
        return add
    raise Exception("cannot form extend")

def pos(func):
    """
Evaluates an XFiniteElement-function assuming a positive level set domain.

Note:
This can lead to non-zero values also in domains where the level set function is non-positive.
    """
    if func.derivname == "pos":
        return func.Deriv()
    add = func.Operator("pos")
    if add:
        return add
    raise Exception("cannot form pos")

def neg(func):
    """
Evaluates an XFiniteElement-function assuming a negative level set domain.

Note:
This can lead to non-zero values also in domains where the level set function is non-negative.
    """
    if func.derivname == "neg":
        return func.Deriv()
    add = func.Operator("neg")
    if add:
        return add
    raise Exception("cannot form neg")

def extend_grad(func):
    """
Evaluates the gradient of an XFiniteElement-function independent of the level set domains.

Note:
This will lead to the same behavior as the function that the XFiniteElement-function is based on.
    """
    if func.derivname == "extendgrad":
        return func.Deriv()
    add = func.Operator("extendgrad")
    if add:
        return add
    raise Exception("cannot form extend_grad")

def pos_grad(func):
    """
Evaluates the gradient of an XFiniteElement-function assuming a positive level set domain.

Note:
This can lead to non-zero values also in domains where the level set function is non-positive.
    """
    if func.derivname == "posgrad":
        return func.Deriv()
    add = func.Operator("posgrad")
    if add:
        return add
    raise Exception("cannot form pos_grad")

def neg_grad(func):
    """
Evaluates the gradient of an XFiniteElement-function assuming a negative level set domain.

Note:
This can lead to non-zero values also in domains where the level set function is non-negative.
    """
    if func.derivname == "neggrad":
        return func.Deriv()
    add = func.Operator("neggrad")
    if add:
        return add
    raise Exception("cannot form neg_grad")

SymbolicBFI_old = SymbolicBFI
def SymbolicBFI(levelset_domain=None, *args, **kwargs):
    """
Wrapper around SymbolicBFI to allow for integrators on level set domains (see also
SymbolicCutBFI). The dictionary contains the level set function (CoefficientFunciton or
GridFunction) and the domain-type (NEG/POS/IF). If the dictionary is not provided, the standard
SymbolicBFI function from NGSolve will be called.

Parameters

levelset_domain : dictionary
  entries:
  * "levelset": ngsolve.CoefficientFunction
    CoefficientFunction that describes the geometry. In the best case lset is a GridFunction of an
    FESpace with scalar continuous piecewise (multi-) linear basis functions.
  * "domain_type" : {NEG,POS,IF} (ENUM)
    Integration on the domain where either:
    * the level set function is negative (NEG)
    * the level set function is positive (POS)
    * the level set function is zero     (IF )
  * "subdivlvl" : int
    On simplex meshes a subtriangulation is created on which the level set function lset is
    interpolated piecewise linearly. Based on this approximation, the integration rule is
    constructed. Note: this argument only works on simplices.
  * "force_intorder" : int
    (default: entry does not exist or value -1)
    overwrites "order"-arguments in the integration

Other Parameters :

  form : ngsolve.CoefficientFunction
    form to integrate

  VOL_or_BND : {VOL,BND}
    integrator is defined in the volume or boundary

  element_boundary : boolean
    Integration of the boundary of an element
    (not active for level set domains)

  skeleton : boolean
    Integration over element-interface

  definedon : Region
    Domain description on where the integrator is defined

  definedonelements: BitArray
    BitArray that allows integration only on elements or facets (if skeleton=True) that are marked
    True.
"""
    if levelset_domain != None and type(levelset_domain)==dict:
        if not "force_intorder" in levelset_domain:
            levelset_domain["force_intorder"] = -1
        if not "subdivlvl" in levelset_domain:
            levelset_domain["subdivlvl"] = 0
        if not "levelset" in levelset_domain:
            print("Please provide a level set function")
        if not "domain_type" in levelset_domain:
            print("Please provide a domain type (NEG,POS or IF)")
        # print("SymbolicBFI-Wrapper: SymbolicCutBFI called")
        return SymbolicCutBFI(lset=levelset_domain["levelset"],
                              domain_type=levelset_domain["domain_type"],
                              force_intorder=levelset_domain["force_intorder"],
                              subdivlvl=levelset_domain["subdivlvl"],
                              *args, **kwargs)
    else:
        # print("SymbolicBFI-Wrapper: original SymbolicBFI called")
        if (levelset_domain == None):
            return SymbolicBFI_old(*args,**kwargs)
        else:
            return SymbolicBFI_old(levelset_domain,*args,**kwargs)

SymbolicLFI_old = SymbolicLFI
def SymbolicLFI(levelset_domain=None, *args, **kwargs):
    """
Wrapper around SymbolicLFI to allow for integrators on level set domains (see also
SymbolicCutLFI). The dictionary contains the level set function (CoefficientFunciton or
GridFunction) and the domain-type (NEG/POS/IF). If the dictionary is not provided, the standard
SymbolicLFI function from NGSolve will be called.

Parameters

levelset_domain : dictionary
  entries:
  * "levelset": ngsolve.CoefficientFunction
    CoefficientFunction that describes the geometry. In the best case lset is a GridFunction of an
    FESpace with scalar continuous piecewise (multi-) linear basis functions.
  * "domain_type" : {NEG,POS,IF} (ENUM)
    Integration on the domain where either:
    * the level set function is negative (NEG)
    * the level set function is positive (POS)
    * the level set function is zero     (IF )
  * "subdivlvl" : int
    On simplex meshes a subtriangulation is created on which the level set function lset is
    interpolated piecewise linearly. Based on this approximation, the integration rule is
    constructed. Note: this argument only works on simplices.
  * "force_intorder" : int
    (default: entry does not exist or value -1)
    overwrites "order"-arguments in the integration

Other Parameters :

  form : ngsolve.CoefficientFunction
    form to integrate

  VOL_or_BND : {VOL,BND}
    integrator is defined in the volume or boundary

  element_boundary : boolean
    Integration of the boundary of an element
    (not active for level set domains)

  skeleton : boolean
    Integration over element-interface

  definedon : Region
    Domain description on where the integrator is defined

  definedonelements: BitArray
    BitArray that allows integration only on elements or facets (if skeleton=True) that are marked
    True.
"""
    if levelset_domain != None and type(levelset_domain)==dict:
        if not "force_intorder" in levelset_domain:
            levelset_domain["force_intorder"] = -1
        if not "subdivlvl" in levelset_domain:
            levelset_domain["subdivlvl"] = 0
        if not "levelset" in levelset_domain:
            print("Please provide a level set function")
        if not "domain_type" in levelset_domain:
            print("Please provide a domain type (NEG,POS or IF)")
        # print("SymbolicLFI-Wrapper: SymbolicCutLFI called")
        return SymbolicCutLFI(lset=levelset_domain["levelset"],
                              domain_type=levelset_domain["domain_type"],
                              force_intorder=levelset_domain["force_intorder"],
                              subdivlvl=levelset_domain["subdivlvl"],
                              *args, **kwargs)
    else:
        # print("SymbolicLFI-Wrapper: original SymbolicLFI called")
        if (levelset_domain == None):
            return SymbolicLFI_old(*args,**kwargs)
        else:
            return SymbolicLFI_old(levelset_domain,*args,**kwargs)

def Integrate_X_special_args(levelset_domain={}, cf=None, mesh=None, VOL_or_BND=VOL, order=5, region_wise=False, element_wise = False, heapsize=1000000):
    """
Integrate_X_special_args should not be called directly.
See documentation of Integrate.
    """
    if not "force_intorder" in levelset_domain or levelset_domain["force_intorder"] == -1:
        levelset_domain["force_intorder"] = -1
    else:
        order = levelset_domain["force_intorder"]

    if not "subdivlvl" in levelset_domain:
        levelset_domain["subdivlvl"] = 0
    if not "levelset" in levelset_domain:
        print("Please provide a level set function")
    if not "domain_type" in levelset_domain:
        print("Please provide a domain type (NEG,POS or IF)")

    return IntegrateX(lset=levelset_domain["levelset"],
                      mesh=mesh, cf=cf,
                      order=order,
                      domain_type=levelset_domain["domain_type"],
                      subdivlvl=levelset_domain["subdivlvl"],
                      heapsize=heapsize)


##### THIS IS ANOTHER WRAPPER (original IntegrateX-interface is pretty ugly...) TODO
Integrate_old = Integrate
def Integrate(levelset_domain=None, *args, **kwargs):
    """
Integrate-wrapper. If a dictionary 'levelset_domain' is provided integration will be done on the
level set part of the mesh. The dictionary contains the level set function (CoefficientFunciton or
GridFunction) and the domain-type (NEG/POS/IF). If the dictionary is not provided, the standard
Integrate function from NGSolve will be called.

Parameters

levelset_domain : dictionary
  entries:
  * "levelset": ngsolve.CoefficientFunction
    CoefficientFunction that describes the geometry. In the best case lset is a GridFunction of an
    FESpace with scalar continuous piecewise (multi-) linear basis functions.
  * "domain_type" : {NEG,POS,IF} (ENUM)
    Integration on the domain where either:
    * the level set function is negative (NEG)
    * the level set function is positive (POS)
    * the level set function is zero     (IF )
  * "subdivlvl" : int
    On simplex meshes a subtriangulation is created on which the level set function lset is
    interpolated piecewise linearly. Based on this approximation, the integration rule is
    constructed. Note: this argument only works on simplices.
  * "force_intorder" : int
    (default: entry does not exist or value -1)
    overwrites "order"-arguments in the integration

mesh :
  Mesh to integrate on (on some part)

cf : ngsolve.CoefficientFunction
  the integrand

order : int (default = 5)
  integration order. Can be overruled by "force_intorder"-entry of the levelset_domain dictionary.

region_wise : bool
  (only active for non-levelset version)

element_wise : bool
  (only active for non-levelset version)

heapsize : int
  heapsize for local computations.
    """
    if levelset_domain != None and type(levelset_domain)==dict:
        # print("Integrate-Wrapper: IntegrateX called")
        return Integrate_X_special_args(levelset_domain, *args, **kwargs)
    else:
        # print("Integrate-Wrapper: original Integrate called")
        if (levelset_domain == None):
            return Integrate_old(*args,**kwargs)
        else:
            newargs = [levelset_domain]
            for q in args:
                newargs.append(q)
            return Integrate_old(*newargs,**kwargs)

def IndicatorCF(mesh, ba, facets = False):
    """
Returns a CoefficientFunction that evaluates a BitArray. On elements/facets with an index i where
the BitArray evaluates to true the CoefficientFunction will evaluate as 1, otherwise as 0. Similar
functionality (only on elements) can be obtained with BitArrayCF.
    """
    if facets:
        ret = GridFunction(FESpace("facet",mesh,order=0))
        for i in range(len(ba)):
            if ba[i]:
                ret.vec[i] = 1.0
            else:
                ret.vec[i] = 0.0
        return ret
    else:
        return BitArrayCF(BitArray(ba))

def CutRatioGF(cutinfo):
    """
Ratio between negative and full part of an element. Vector taken from CutInfo and put into a
piecewise constant GridFunction.
    """
    ret = GridFunction(L2(cutinfo.Mesh(),order=0))
    ret.vec.data = cutinfo.GetCutRatios(VOL)
    return ret

def kappa(mesh,lset_approx, subdivlvl=0):
    """
Tuple of ratios between negative/positive and full
part of an element (deprecated).
    """
    print("kappa-function is deprecated - use CutRatioGF instead")
    kappa1 = GridFunction(L2(mesh,order=0))
    lset_neg = { "levelset" : lset_approx, "domain_type" : NEG, "subdivlvl" : subdivlvl}
    kappa_f = LinearForm(kappa1.space)
    kappa_f += SymbolicLFI(levelset_domain = lset_neg, form = kappa1.space.TestFunction() )
    kappa_f.Assemble();
    kappa1.space.SolveM(CoefficientFunction(1.0),kappa_f.vec)
    kappa1.vec.data = kappa_f.vec
    kappa2 = 1.0 - kappa1
    return (kappa1,kappa2)

def IsCut(mesh,lset_approx, subdivlvl=0):
    """
GridFunction that is 1 on cut elements, 0 otherwise (deprecated). Use CutInfo-functionality (perhaps
combined with BitArrayCF).
    """
    print("IsCut-function is deprecated - use CutInfo-functionality instead")
    def cut(kappa):
        if (kappa > 1e-16 and kappa < 1.0-1e-16):
            return 1.0
        else:
            return 0.0
    kappa1, dummycf = kappa(mesh,lset_approx,subdivlvl)
    for i in range(len(kappa1.vec)):
        kappa1.vec[i] = cut(kappa1.vec[i])
    # from numpy import vectorize
    # cut = vectorize(cut)
    # kappa1.vec.FV().NumPy()[:] = cut(kappa1.vec.FV().NumPy())
    return kappa1
