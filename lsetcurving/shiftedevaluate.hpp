#ifndef FILE_SHIFTEDEVALUATE_HPP
#define FILE_SHIFTEDEVALUATE_HPP

#include <fem.hpp>   // for ScalarFiniteElement
#include <ngstd.hpp> // for Array
#include <comp.hpp>

using namespace ngcomp;
namespace ngfem
{

  template <int D>
  class DiffOpShiftedEval : public DifferentialOperator
  {


  public:

    shared_ptr<GridFunction> back;
    shared_ptr<GridFunction> forth;

    enum { DIM = D };          // D copies of the spaces
    enum { DIM_SPACE = 2 };    // D-dim space
    enum { DIM_ELEMENT = 2 };  // D-dim elements (in contrast to boundary elements)
    enum { DIM_DMAT = D };     // D-matrix
    enum { DIFFORDER = 0 };    // minimal differential order (to determine integration order)

    DiffOpShiftedEval(shared_ptr<GridFunction> aback,shared_ptr<GridFunction> aforth)
      : DifferentialOperator(DIM_DMAT, 1, VorB(int(DIM_SPACE)-int(DIM_ELEMENT)), DIFFORDER),
        back(aback), forth(aforth)
    {
      //dimensions = DIFFOP::GetDimensions();
      dimensions = Array<int> ( { DIM_DMAT } );

    }
    /*
    virtual int Dim() const { return DIM_DMAT; }
    virtual bool Boundary() const { return int(DIM_SPACE) > int(DIM_ELEMENT); }
    virtual int DiffOrder() const { return DIFFORDER; }
    */
    virtual string Name() const { return "Fix_time"; }

    virtual bool operator== (const DifferentialOperator & diffop2) const
    { return typeid(*this) == typeid(diffop2); }


    virtual void
    CalcMatrix (const FiniteElement & bfel,
        const BaseMappedIntegrationPoint & bmip,
        SliceMatrix<double,ColMajor> mat,
        LocalHeap & lh) const;


    virtual void
    Apply (const FiniteElement & fel,
           const BaseMappedIntegrationPoint & mip,
           FlatVector<double> x, 
           FlatVector<double> flux,
           LocalHeap & lh) const;
    
    virtual void
    ApplyTrans (const FiniteElement & fel,
        const BaseMappedIntegrationPoint & mip,
        FlatVector<double> flux,
        FlatVector<double> x,
        LocalHeap & lh) const;

  };



}
#endif
