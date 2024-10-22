# https://journals.aps.org/prab/pdf/10.1103/PhysRevAccelBeams.22.121002
def get_impedance(offsets, R, f0, Q, omega, plot=False):
    
        RoverQ = R/Q
        a,b,c = np.polyfit(offsets*1e-3, RoverQ, deg = 2)
        
        x = np.linspace(0,np.amax(offsets)*1e-3,10000)
        y = a*np.square(x) + b*x + c
        
        dy = 2*a*x + b
        d2y = 2*a
        
        if plot == True:
            fig, ax = plt.subplots()

            ax.scatter(offsets*1e-3, RoverQ)
            ax.plot(x, y)
        
        cl = 3e8

        omega0 = 2*np.pi*f0*1e9
        g = Q/(1+1j*Q*(omega/omega0-omega0/omega))

        Z_quad = (cl*g/(4*omega))* (-np.square(dy[0])/y[0] + 2*d2y)
        Z_dip = (cl*g/(4*omega))* np.square(dy[0])/y[0]
        
        if R[0] < 2:
            Z_dip = cl/2/omega*d2y*g
        
        return Z_quad, Z_dip