# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 14:14:36 2020

@author: Louie
"""

import numpy as np
import matplotlib.pyplot as plt

def sequence(n):
    """
    Description
    -----------
    A basic implenetation of a Collatz Sequence. For a given n you repeatedly 
    apply the rules of n-> n/2 if n%2=0 and n-> 3n+1 if n%2=1, according to 
    the collataz Conjecture this will terminate at 1 for any given n.
    
    Parameters
    ----------
    n: int, the number that you wish to find the collatz sequence for
    Returns
    -------
    sequence : list
        The Collatz Sequence for the inputed n
    """
    sequence=[]
    sequence.append(n)
    while n!=1:
        if n%2==0:
            n=n/2
            sequence.append(n)
        else:
            n=3*n+1
            sequence.append(n)
    return sequence         
            

def sequence_array(n):
    """
    Description
    -----------
    A vectorised implemntation to find the collatz sequence for the first n 
    numvers. For a each number the rules n-> n/2 if n%2=0 and n-> 3n+1 if n%2=1,
    are repeatdly applied. according to the collataz Conjecture this will 
    terminate at 1 for any given n.
    
    Parameters
    ----------
    n: int, the number of collatz sequence you want (0 to n)
    Returns
    -------
    sequence : array
        The Sequence for all integrs from 0 to n
    """
    num=np.linspace(1,n,n)
    sequence=np.linspace(1,n,n)
    
    m=np.ones(num.shape,dtype=bool)
    o=np.ones(num.shape,dtype=bool)
    condition=True
    step=0
    
    while condition:
        
        m=num%2==0
        o=((num%2==1) & (num!=1))
        num[m]=num[m]/2
        num[o]=(num[o]*3+1)/2
        m=num%2==0
        o=((num%2==1) & (num!=1))
    
        condition=any(o)+any(m)
        sequence=np.vstack([sequence,num])
        step=step+1
    return sequence         
            
def prep(sequence):
    """
    Description 
    -----------
    A helper function that preps the subarrays from sequence_array() for plotting.
    It removes any excess ones and reverses the order.
    
    Parameters
    ----------
    sequence: array, the collataz array to be prepped
    Returns
    -------
    sequence : array
        The Sequence ready to be plotted
    """
    index= sequence.tolist().index(1)
    sequence=sequence[:index+1]
    sequence=sequence[::-1]
    return sequence

def rotate(origin, point, angle):
    """
    Description
    -----------
    A helper function that rotates a point about an origin by a given angle in 
    the counter-clockwise direction.
    
    Parameters
    ----------
    origin: float, anchor point for the rotation 
    point: float, end point of rotation
    angle: float, angle to rotate through
    -------
    qx, new x position of rotated point
    qy, new y position of rotated point

    """
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return qx, qy


def curve_sequence(sequence,a,b,scale=10):
    """
    Description
    -----------
    Curves the collataz sequence according to the pairty of a given point.
    Even points are curved counter-clockwise and odd points clockwise. As such
    Parameters
    ----------
    sequence: array, array of points in collatz sequence
    a: float, angle to rotate counter clockwise
    b: float, angle to rotate clockwise
    scale: effectively stepsize (looks nicer to use a fixed stepsize)
    -------
    temp_x, new x data for curved sequence
    temp_y, new y data for curved sequence
    """
    step=sequence
    temp_x=[0,step[0]]
    temp_y=[1,1]
    for j in range(1,len(step)):
        
        old_point=np.array([temp_x[j],temp_y[j]])
        x=(temp_x[j]-temp_x[j-1])
        y=(temp_y[j]-temp_y[j-1])
        mag=np.linalg.norm([x,y])
        norm=np.array([x,y]/mag)
        
        if step[j]%2==0:
            point=old_point+scale*norm
            x_pos,y_pos=rotate(old_point,point,a)
            temp_x.append(x_pos)
            temp_y.append(y_pos)
        else:
            point=old_point+scale*norm
            x_pos,y_pos=rotate(old_point,point,-b)
            temp_x.append(x_pos)
            temp_y.append(y_pos)
        
    return temp_x,temp_y
        
        
def plot(sequence,a,b,scale):
    """
    Description
    -----------
    Plots each collatz sequence on a singel canvas. Inefficient, consider using
    line collections
    
    Parameters
    ----------
    sequence: array, array of  collatz sequences
    a: float, angle to rotate counter clockwise
    b: float, angle to rotate clockwise
    scale: effectively stepsize (looks nicer to use a fixed stepsize)
    -------

    """
    
    sequence=sequence.transpose()
   
    plt.figure(1,figsize=(19.20,10.80))
    plt.clf()
    plt.style.use('dark_background')
    plt.axis('off')
    for i in range(len(sequence)):
        step=prep(sequence[i])
        ctrl=max(step)
        x,y=curve_sequence(step,a,b,scale)
        width = 1.5+1/(ctrl**0.025)
        opacity=0.005+0.8/(ctrl**0.5)
        
        plt.plot(x,y,linewidth=width,alpha=0.05,color="white")
        plt.show()
    
        
 
def animate(n,m,scale):
    """
    Description
    -----------
    Saves the frames of an animaiton which can be turned into a gif.
    
    Parameters
    ----------
    n: int, the amount of collatz sequences
    m: the stepsize in the angle
    scale: effectively stepsize (looks nicer to use a fixed stepsize)
    -------

    """
    
    sequence=sequence_array(n)
    a=np.linspace(0,0.2,m)
    b=np.linspace(0,0.3,m)
    for i in range(len(a)):
        plot(sequence,a[i],b[i],scale)
        plt.savefig("%s"%(i))
    
 
def run(n,a,b,scale):
    sequence=sequence_array(n)
    plot(sequence,a,b,scale)
    plt.savefig("random", dpi=300)



run(5000,0.3,0.265,1.2)
    