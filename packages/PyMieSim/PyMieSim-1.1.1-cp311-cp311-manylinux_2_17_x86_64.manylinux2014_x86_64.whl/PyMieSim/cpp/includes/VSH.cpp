#ifndef VSH_H
  #define VSH_H

#include "definitions.cpp"
#include "fibonnaci_mesh.cpp"


namespace VSH{
    namespace SPHERICAL {

        CVector compute_dn(double &&nmx, complex128 &z) //Page 127 of BH
        {
          CVector Dn(nmx, 0.0);

          for (double n = nmx - 1.; n > 1.; n--)
              Dn[n-1] = n/z - ( 1. / (Dn[n] + n/z) );

           return Dn;
        }

        inline std::tuple<CVector, CVector> MiePiTau(double &mu, size_t &max_order)
        {
          CVector pin, taun;
          pin.reserve(max_order);
          taun.reserve(max_order);

          pin.push_back( 1. );
          pin.push_back( 3. * mu );

          taun.push_back( mu );
          taun.push_back( 3.0 * cos(2. * acos(mu) ) );

          double n = 0;
          for (uint i = 2; i < max_order; i++)
              {
               n = (double)i;

               pin.push_back( ( (2. * n + 1.) * mu * pin[i-1] - (n + 1.) * pin[i-2] ) / n );

               taun.push_back( (n + 1.) * mu * pin[i] - (n + 2.) * pin[i-1] );
             }

          return std::make_tuple(pin, taun);
        }


        inline std::tuple<CVector, CVector> MiePiTau(double &mu, size_t &&max_order)
        {
          CVector pin, taun;
          pin.reserve(max_order);
          taun.reserve(max_order);

          pin.push_back( 1. );
          pin.push_back( 3. * mu );

          taun.push_back( mu );
          taun.push_back( 3.0 * cos(2. * acos(mu) ) );

          double n = 0;
          for (uint i = 2; i < max_order; i++)
              {
               n = (double)i;

               pin.push_back( ( (2. * n + 1.) * mu * pin[i-1] - (n + 1.) * pin[i-2] ) / n );

               taun.push_back( (n + 1.) * mu * pin[i] - (n + 2.) * pin[i-1] );
             }

          return std::make_tuple(pin, taun);
        }



        inline void MiePiTau(double mu, uint max_order, complex128 *pin, complex128 *taun)
        {
          pin[0] = 1.;
          pin[1] = 3. * mu;

          taun[0] = mu;
          taun[1] = 3.0 * cos(2. * acos(mu) );

          double n = 0;
          for (uint i = 2; i < max_order; i++)
              {
               n = (double)i;

               pin[i] = ( (2. * n + 1.) * mu * pin[i-1] - (n + 1.) * pin[i-2] ) / n;

               taun[i] = (n + 1.) * mu * pin[i] - (n + 2.) * pin[i-1];
             }
        }




        SCoordinate RDir(double &theta, double &phi)
        {
            SCoordinate Output;
            Output.R     = sin(theta)*cos(phi);
            Output.Phi   = sin(theta)*sin(phi),
            Output.Theta = cos(theta);
            return Output;
        }

        SCoordinate ThetaDir(double &theta, double &phi)
        {
            SCoordinate Output;
            Output.R     = cos(theta)*cos(phi);
            Output.Phi   = cos(theta)*sin(phi),
            Output.Theta = -sin(theta);
            return Output;
        }

        SCoordinate PhiDir(double &theta, double &phi)
        {
            SCoordinate Output;
            Output.R     = -sin(phi);
            Output.Phi   = cos(phi),
            Output.Theta = 0;
            return Output;
        }







    }




    namespace CYLINDRICAL {

      CVector compute_dn(double &&nmx, complex128 &z) //Page 205 of BH
      {
        CVector Dn(nmx, 0.0);

        for (double n = nmx - 1; n > 0; n--)
            Dn[n-1] = n/z - ( 1. / (Dn[n] + n/z) );

         return Dn;
      }

    }







}


#endif
