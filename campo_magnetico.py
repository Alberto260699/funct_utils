import numpy as np
import matplotlib.pyplot as plt
from magpylib.source.current import Circular
from magpylib import Collection, displaySystem

#geometry variables
current=20 #A
outer_d=684 #mm
inner_d=460 #mm
Nloops=14
thickness=15 #mm #spessore
stack=2 #pila
Ncoils=3
coil_distance=240 #mm

#Variables for coil design
pipe_d=(outer_d-inner_d)/float(Nloops)
pipe_t=thickness/float(stack)

#empty list for sources
sources=[]

#create coils
for k in range(0, Ncoils):
    if k==1:
        curr=current
    else:
        curr=current
    for i in range(0, stack):
        for j in range(0, Nloops):
            sources.append(Circular(curr=curr, dim=inner_d+j*pipe_d, pos=(0., 0., k*coil_distance+i*pipe_t)))
            
# create collection
c=Collection(sources)

# calculate B-field on a grid
xs=np.linspace(-350,350,100)
zs=np.linspace(-150,650,100)
POS=np.array([(x,0,z) for z in zs for x in xs])
Bs=c.getB(POS).reshape(100,100,3)     #<--VECTORIZED

#create figure
fig=plt.figure(figsize=(9,5))
ax1=fig.add_subplot(121, projection='3d')  # 3D-axis
ax2=fig.add_subplot(122)                   # 2D-axis

#display system geometry on ax1
displaySystem(c, subplotAx=ax1, suppress=True)

#display field in xz-plane using matplotlib
X,Z=np.meshgrid(xs,zs) #Return coordinate matrices from coordinate vectors.
U,V=Bs[:,:,0], Bs[:,:,2]
strm=ax2.streamplot(X, Z, U, V, color=np.log(U**2+V**2), cmap='plasma')
fig.colorbar(strm.lines)

plt.savefig('Inverse_coil.png')
plt.show()