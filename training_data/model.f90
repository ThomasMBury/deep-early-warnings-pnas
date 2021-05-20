!----------------------------------------------------------------------
!----------------------------------------------------------------------
!   model: Fortran script to specify model for AUTO
!----------------------------------------------------------------------
!----------------------------------------------------------------------

      SUBROUTINE FUNC(NDIM,U,ICP,PAR,IJAC,F,DFDU,DFDP)
!     ---------- ----

      IMPLICIT NONE
      INTEGER, INTENT(IN) :: NDIM, ICP(*), IJAC
      DOUBLE PRECISION, INTENT(IN) :: U(NDIM), PAR(*)
      DOUBLE PRECISION, INTENT(OUT) :: F(NDIM)
      DOUBLE PRECISION, INTENT(INOUT) :: DFDU(NDIM,NDIM), DFDP(NDIM,*)

      DOUBLE PRECISION x,y,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10

       x=U(1)
       y=U(2)
       a1=PAR(1)
       a2=PAR(2)
       a3=PAR(3)
       a4=PAR(4)
       a5=PAR(5)
       a6=PAR(6)
       a7=PAR(7)
       a8=PAR(8)
       a9=PAR(9)
       a10=PAR(10)
!------omit PAR(11) since saved for AUTO computing period
       b1=PAR(12)
       b2=PAR(13)
       b3=PAR(14)
       b4=PAR(15)
       b5=PAR(16)
       b6=PAR(17)
       b7=PAR(18)
       b8=PAR(19)
       b9=PAR(20)
       b10=PAR(21)

       F(1) = a1 + a2*x + a3*y + a4*x**2 + a5*x*y + a6*y**2 + a7*x**3 + a8*x**2*y + a9*x*y**2 + a10*y**3
       F(2) = b1 + b2*x + b3*y + b4*x**2 + b5*x*y + b6*y**2 + b7*x**3 + b8*x**2*y + b9*x*y**2 + b10*y**3
       
      END SUBROUTINE FUNC


      SUBROUTINE STPNT(NDIM,U,PAR,T)

      END SUBROUTINE STPNT

      SUBROUTINE BCND
      END SUBROUTINE BCND

      SUBROUTINE ICND
      END SUBROUTINE ICND

      SUBROUTINE FOPT
      END SUBROUTINE FOPT

      SUBROUTINE PVLS
      END SUBROUTINE PVLS
