#ifndef BASE_SCATTERER_H
#define BASE_SCATTERER_H

  #include "definitions.cpp"
  #include "utils.cpp"
  #include "sources.cpp"
  #include "fibonnaci_mesh.cpp"


class ScatteringProperties
{
public:
    size_t max_order;
    double size_parameter, area;
    SOURCE::State source;

    virtual std::tuple<std::vector<complex128>, std::vector<complex128>> compute_s1s2(const std::vector<double> &Phi){};
    virtual double get_Qsca(){};
    virtual double get_Qext(){};
    virtual double get_Qback(){};
    virtual double get_g(){};

    ScatteringProperties(){}

    ScatteringProperties(double &wavelength, std::vector<complex128> &jones_vector, double &amplitude) : source(wavelength, jones_vector, amplitude){}

    ScatteringProperties(SOURCE::State &source) : source(source){}

    double get_Qforward(){return get_Qsca() - get_Qback();};
    double get_Qpr(){return get_Qext() - get_g() * get_Qsca();};
    double get_Qratio(){return get_Qback() / get_Qsca();};
    double get_Qabs(){return get_Qext() - get_Qsca();};
    double get_Csca(){return get_Qsca() * area;};
    double get_Cext(){return get_Qext() * area;};
    double get_Cabs(){return get_Qabs() * area;};
    double get_Cback(){return get_Qback() * area;};
    double get_Cforward(){return get_Qforward() * area;};
    double get_Cpr(){return get_Qpr() * area;};
    double get_Cratio(){return get_Qratio() * area;};

    std::vector<double>
    get_prefactor()
    {
        std::vector<double> output;
        output.reserve(max_order);

        for (size_t m = 0; m < max_order ; ++m)
            output[m] = (double) ( 2 * (m+1) + 1 ) / ( (m+1) * ( (m+1) + 1 ) );

        return output;
    }

    complex128 compute_propagator(const double &radius)
    {
        return source.amplitude / (source.k * radius) * exp(-JJ * source.k * radius);
    }

    std::tuple<std::vector<complex128>, std::vector<complex128>>
    compute_structured_fields(const std::vector<complex128>& S1,
                              const std::vector<complex128>& S2,
                              const std::vector<double>& theta,
                              const double& radius)
    {
        std::vector<complex128> phi_field, theta_field;

        size_t full_size = theta.size() * S1.size();

        phi_field.reserve(full_size);
        theta_field.reserve(full_size);

        complex128 propagator = this->compute_propagator(radius);

        for (uint p=0; p < S1.size(); p++ )
            for (uint t=0; t < theta.size(); t++ )
            {
                complex128 phi_point_field = propagator * S1[p] * (source.jones_vector[0] * cos(theta[t]) + source.jones_vector[1] * sin(theta[t]));
                complex128 thetea_point_field = propagator * S2[p] * (source.jones_vector[0] * sin(theta[t]) - source.jones_vector[1] * cos(theta[t]));

                phi_field.push_back(phi_point_field);
                theta_field.push_back(thetea_point_field);
            }

        return std::make_tuple(
            phi_field,
            theta_field
        );
    }


    std::tuple<std::vector<complex128>, std::vector<complex128>>
    compute_unstructured_fields(const std::vector<double>& phi,
                                const std::vector<double>& theta,
                                const double radius=1.0)
    {
        auto [S1, S2] = this->compute_s1s2(phi);

        std::vector<complex128> phi_field, theta_field;

        size_t full_size = theta.size();

        phi_field.reserve(full_size);
        theta_field.reserve(full_size);

        complex128 propagator = this->compute_propagator(radius);

        for (uint idx=0; idx < full_size; idx++)
        {
            complex128 phi_field_point = propagator * S1[idx] * (source.jones_vector[0] * cos(theta[idx]) + source.jones_vector[1] * sin(theta[idx])),
            theta_field_point = propagator * S2[idx] * (source.jones_vector[0] * sin(theta[idx]) - source.jones_vector[1] * cos(theta[idx]));

            phi_field.push_back(phi_field_point);
            theta_field.push_back(theta_field_point);
        }

        return std::make_tuple(phi_field, theta_field);
    }

    std::tuple<std::vector<complex128>, std::vector<complex128>>
    compute_unstructured_fields(const FibonacciMesh& Mesh, const double radius=1.0)
    {
        return this->compute_unstructured_fields(
            Mesh.SCoord.Phi,
            Mesh.SCoord.Theta,
            radius
        );
    }


    std::tuple<std::vector<complex128>, std::vector<complex128>, std::vector<double>, std::vector<double>>
    compute_full_structured_fields(size_t& sampling, double& radius)
    {
        FullSteradian full_mesh = FullSteradian(sampling);

        auto [S1, S2] = this->compute_s1s2(full_mesh.SCoord.Phi);

        auto [phi_field, theta_field] = this->compute_structured_fields(
            S1,
            S2,
            full_mesh.SCoord.Theta,
            radius
        );

        return std::make_tuple(
            phi_field,
            theta_field,
            full_mesh.SCoord.Phi,
            full_mesh.SCoord.Theta
        );
    }


    std::tuple<std::vector<complex128>, FullSteradian>
    compute_full_structured_spf(size_t sampling, double radius=1.0)
    {
        FullSteradian full_mesh = FullSteradian(sampling);

        auto [phi_field, theta_field] = this->compute_structured_fields(
            full_mesh.SCoord.Phi,
            full_mesh.SCoord.Theta,
            radius
        );

        Squared(phi_field);
        Squared(theta_field);

        std::vector<complex128> spf = Add(phi_field, theta_field);

        return std::make_tuple(spf, full_mesh);
    }

    std::tuple<std::vector<complex128>, std::vector<complex128>>
    compute_structured_fields(const std::vector<double>& phi,
                              const std::vector<double>& theta,
                              const double radius)
    {
      complex128 propagator = this->compute_propagator(radius);

      auto [S1, S2] = this->compute_s1s2(phi);

      return this->compute_structured_fields(S1, S2, theta, radius);
    }

    //--------------------------------------------------------PYTHON-------------------


    std::tuple<Cndarray,Cndarray> get_s1s2_py(const std::vector<double> &phi)
    {
        auto [S1, S2] = this->compute_s1s2(phi);

        return std::make_tuple(
            vector_to_ndarray(S1),
            vector_to_ndarray(S2)
        );
    }


    std::tuple<Cndarray, Cndarray, ndarray, ndarray>
    get_full_structured_fields_py(size_t &sampling, double& R)
    {
        auto [phi_field, theta_field, theta, phi] = this->compute_full_structured_fields(sampling, R);

        Cndarray phi_field_py = vector_to_ndarray(phi_field, {sampling, sampling}),
        theta_field_py = vector_to_ndarray(theta_field, {sampling, sampling});

        ndarray  theta_py = vector_to_ndarray(theta),
        phi_py = vector_to_ndarray(phi);

        phi_field_py = phi_field_py.attr("transpose")();
        theta_field_py = theta_field_py.attr("transpose")();

        return std::make_tuple(
            phi_field_py,
            theta_field_py,
            phi_py,
            theta_py
        );
    }

    std::tuple<Cndarray,Cndarray>
    get_unstructured_fields_py(const std::vector<double>& phi, const std::vector<double>& theta, const double r)
    {
        auto [theta_field, phi_field] = this->compute_unstructured_fields(phi, theta, r);

        return std::make_tuple(
            vector_to_ndarray(phi_field),
            vector_to_ndarray(theta_field)
        );
    }



    double get_g_with_fields(size_t sampling, double R)
    {
        auto [SPF, Mesh] = this->compute_full_structured_spf(sampling, R);

        double norm = abs(Mesh.Integral(SPF)),
               expected_cos = abs( Mesh.IntegralCos(SPF) );

        return expected_cos/norm;
    }

};

#endif
