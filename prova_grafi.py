import numpy as np
import matplotlib.pyplot as plt

x=np.arange(0,10,0.1)
fig=plt.figure(figsize=(10,7))

ax1=fig.add_subplot(231)
ax1.plot(x, 2**(1/x))
ax1.set_title('2**(1/x)')
plt.grid(linestyle='--')

ax2=fig.add_subplot(232)
ax2.plot(x, np.sqrt(x))
ax2.set_title('sqrt(x)')
plt.grid(linestyle='--')

ax3=fig.add_subplot(233)
ax3.plot(x, x**2)
ax3.set_title('x**2')
plt.grid(linestyle='--')

ax4=fig.add_subplot(234)
ax4.plot(x, 1/x)
ax4.set_title('1/x')
plt.grid(linestyle='--')

ax5=fig.add_subplot(235)
ax5.plot(x, 1-np.exp(-x))
ax5.set_title('1-exp(-x)')
plt.grid(linestyle='--')

ax6=fig.add_subplot(236)
ax6.plot(x, np.log(x))
#ax6.plot(x, 4*x**2*np.exp(-2*x)*(1-1/2.7))
ax6.set_title('log(x)')
plt.grid(linestyle='--')

plt.show()