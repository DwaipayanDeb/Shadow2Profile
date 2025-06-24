# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Copyright: Dwaipayan Deb @ 2024

import numpy as np
import random
import time
import os
from tablefile import *
from datetime import datetime
from shadowClass import SurfaceCurve
from matplotlib import pyplot as plt
import json


try:
    f=file("shadow_pattern.csv",",")
except:
    print("File not found!\nPlease create a 'shadow_pattern.csv' file first.")
    print("Exiting...")
    exit()

f2=open("output.txt",'a')
f3=open("profile.csv",'w')
#----------------------Starting parameters-------------------

m_lr=np.tan(np.deg2rad(10)) # Slope of the light ray (default 10 deg.)
Trials=300 # Number of attempts to find a best fit

s_range1=np.arange(0.001,0.011,0.001) # Range for s values
s_range2=np.arange(0.01,0.11,0.01) # Range for s values
h_range=np.arange(0.001,0.011,0.001) # Range for h values
#---------------------------------------------------------------

def load_settings(filename):
    try:
        with open(filename, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print("Settings file not found. Using default settings.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON. Using default settings.")
        return None

loaded_settings = load_settings('.\settings.json')
divisions=loaded_settings["divisions"]


while True:
    beta=input('\nAngle of light incidence measuered clockwise in degrees (Default is 80 deg.)?:')
    if beta.isdigit():
        beta=int(beta)
        if beta<90:
            m_lr=np.tan(np.deg2rad(90-beta))
            break
        else:
            print("Angle of incidence should be less than 90 degree")
    else:
        break

        #print(m_lr)

print(f"\nScale-factor ranges are:\ns_range1=[{round(min(s_range1),3)},{round((max(s_range1)),2)}]")
print(f"s_range2=[{round(min(s_range2),3)},{round(max(s_range2),2)}]")
print(f"\nMaximum height range is:\nh_range=[{round(min(h_range),3)},{round(max(h_range),2)}]")

print("\nStarting with s_range2")
s_range=2            # range2 is faster therefore it is selected by default
answer=input('Would you like to proceed with s_range1 instead (Y/N)?')
if answer=="Y" or answer=="y":
    s_range=1



while True:
    start_time=time.time()

    if s_range==1:
        xedges=s_range1
    else:
        xedges=s_range2
    yedges=h_range


    Shadow_image=[]

    Shadow_image=f.read()
    Shadow_image.reverse()
    #----------------------------------------------------------

    length = 1 #Total length of the straight line on the surface (Unit length case)

    def area(y1, y2, l): # l is baseline
        if (y1 * y2 > 0):
            return (l / 2) * (abs(y1 + y2))
        else:
            return (l / 2) * ((y1**2 + y2**2) / (abs(y1) + abs(y2)))

    def slope(y1, y2, l): # l is baseline
        return (abs(y1 - y2) / l)

    def lineParams(point1,point2): #([x1,y1],[x2,y2])
        m=(point2[1]-point1[1])/(point2[0]-point1[0])
        c=point1[1]-m*point1[0]
        return[m,c]

    def y_value(m,c,x):
        return m*x+c

    def shadow_profile(scale_factor,height,m_lr):
        x = []
        y = []
        L = 0  # Incremental length of the straight line
        A = 0  # Icremental area enclosed at the line by the curve
        l = 0  # This is delta_L (step for increment)

        while L < length:
            x.append(L)
            y.append(random.choice([-1, 1]) * random.uniform(0, height))
            l = random.uniform(0, scale_factor)
            L = L + l
        x.append(length) # includes the last value
        y.append(random.choice([-1, 1]) * random.uniform(0, height)) # includes the last value

        #print(len(x), len(y))

        x = np.array(x)

        mc=[]
        for i in range(len(x)-1):
            mc.append(lineParams([x[i],y[i]],[x[i+1],y[i+1]])) # mc contains a list of [m,c] values for all the line segments 
            A=A+area(y[i],y[i+1],x[i+1]-x[i]) # Sum of Area below a line on x axis
            #print(area(y[i],y[i+1],x[i+1]-x[i]))
        Ra=A/length 
        Shadow_pattern=[]
        k=len(y)

        for i in reversed(range(1,len(y))):
            flag=False
            if (i<=k):
                c_lr=y[i]-m_lr*x[i] # Intercept of current light ray 
                mc_lr=[m_lr,c_lr]
                if not (mc[i-1][0]<0 or mc[i-1][0]<=m_lr): # Skipping no-shadow cases
                    l_shadow=0 #shadow length
                    for j in reversed(range(0,i)):
            
                        if y_value(m_lr,c_lr,x[j])>y[j]:
                            l_shadow+=x[j+1]-x[j]
                            if j==0:
                                l_shadow=x[i]
                                Shadow_pattern.append([x[i],l_shadow])
                                #plt.plot([x[i], x[i]+0.1], [y[i], m_lr*(x[i]+0.1)+c_lr], color='red', linestyle='--')
                                flag=True #############################
                                break
                        else:
                            M=np.array([[mc_lr[0],-1],[mc[j][0],-1]])
                            C=np.array([-mc_lr[1],-mc[j][1]])
                            B=np.linalg.solve(M,C) # B gives insersection point of light and a line segment
                            if B[0]>0:
                                l_shadow+=x[j+1]-B[0]
                            else:
                                l_shadow+=x[j+1]
                                k=0
                                B[0]=0                
                            k=j
                            #print(x)
                            Shadow_pattern.append([x[i],l_shadow]) 
                            #plt.plot([x[i], x[i]+0.1], [y[i], m_lr*(x[i]+0.1)+c_lr], color='red', linestyle='--')
                            break
            if flag:   ###############################
                break 
        Slope=0
        for val in mc:
            Slope=Slope+np.degrees(np.arctan(abs(val[0]))) #Adding magnitude of slopes only
        Av_Slope=Slope/len(mc)

        return x,y,Shadow_pattern,Av_Slope,Ra               


    def weighted_2d_std(matrix, x_values, y_values, point): # If 'point' represents the mean then the result is S.D. otherwize it is called Mean Absolute Deviation (MAD) or Deviation from a point 
        # Extract the reference point (x_0, y_0)
        x_0, y_0 = point
        X, Y = np.meshgrid(x_values, y_values)
        #print(X)
        squared_distances = (X - x_0)**2 + (Y - y_0)**2
        total_freq = np.sum(matrix)

        # Calculate the weighted sum of squared deviations
        weighted_squared_deviation_sum = np.sum(matrix * squared_distances)

        # Calculate the weighted variance
        weighted_variance = weighted_squared_deviation_sum / total_freq

        # Calculate the weighted standard deviation (square root of variance)
        weighted_std = np.sqrt(weighted_variance)

        return weighted_std




    delta_min=1000
    x_min=[]
    y_min=[]
    Shadow_pattern_min=[]
    Av_Slope_min_list=[]
    scale_min_list=[]
    height_min_list=[]
    sc_h_min_list=[]
    height_min=0
    scale_min=0
    Av_Slope_min=0
    Ra_min=0
    t=0
    scale_factor=0

    height=0



    shadow_vals=[item[1] for item in Shadow_image]
    Av_shadow_length1=sum(shadow_vals)/len(Shadow_image)
    Av_illumin_length1=(1/len(Shadow_image)-Av_shadow_length1)

    print("Starting calculation...\nPlease wait")
    progress=0
    while t < Trials:
        t+=1
        print(f"\rProgress:{round((t/Trials)*100,1)}%",end="")
        for scale_factor in xedges:
            for height in yedges:
                x,y,Shadow_pattern,Av_Slope,Ra=shadow_profile(scale_factor,height,m_lr)
                    #print(Shadow_pattern)
                if len(Shadow_pattern)!=0:
                    mismatch=100000   # This value is 0 for perfect match
                    shadow_vals=[item[1] for item in Shadow_pattern]
                    Av_shadow_length2=sum(shadow_vals)/len(Shadow_pattern)
                    Av_illumin_length2=(1/len(Shadow_pattern)-Av_shadow_length2)
                    
                    mismatch=abs(Av_shadow_length1-Av_shadow_length2)+abs(Av_illumin_length1-Av_illumin_length2) # Analogus to Manhattan Distance
                    if mismatch<delta_min:
                        delta_min=mismatch
                        x_min=x
                        y_min=y
                        Shadow_pattern_min=Shadow_pattern
                        Av_Slope_min=Av_Slope
                        Ra_min=Ra
                        height_min=height
                        scale_min=scale_factor     
        Av_Slope_min_list.append(Av_Slope_min)
        scale_min_list.append(scale_min)
        height_min_list.append(height_min)
        sc_h_min_list.append([scale_min,height_min])
        delta_min=10000  # resetting the value for next trial
        #print(f"Time taken={(time.time()-start_time)/60} minutes")

    Scale_Min_average=sum(scale_min_list)/len(scale_min_list)
    height_Min_average=sum(height_min_list)/len(height_min_list)


    hist_matrix=[]
    rows=[]

    for item_x in xedges:
        for item_y in yedges:
            element=[item_x,item_y]
            rows.append(sc_h_min_list.count(element))
        hist_matrix.append(rows)
        rows=[]
    hist=np.array(hist_matrix)
    #print(hist.T) # Transpose is required to make rows as X-axis, and columns as Y-axis.
    (y_index,x_index) = np.unravel_index(np.argmax(hist.T), hist.shape)
    mode=[xedges[x_index],yedges[y_index]]
    #print(mode)
    mean=[Scale_Min_average,height_Min_average]
    MAD_mode=weighted_2d_std(hist.T,xedges,yedges,mode) # Mean Absolute deviation from Mode (or SD_mode)
    SD=weighted_2d_std(hist.T,xedges,yedges,mean) # Standard Deviation (or SD_mean)

    print("\n\nBest fitted values:")
    print("(s_b,h_b)Mode=",mode)
    print("(s_b,h_b)Mean=",mean)
    print()
    print("Now calculating average slope and Ra value....")

    Av_slopes_result_mode=[]
    Ra_results_mode=[]
    for i in range(1000):
        surface = SurfaceCurve(mode[0],mode[1],m_lr)
        Av_slopes_result_mode.append(surface.calculate_average_slope())
        Ra_results_mode.append(surface.Ra)
    Final_Av_slope_from_mode=(sum(Av_slopes_result_mode)/len(Av_slopes_result_mode))
    Final_Ra_from_mode=sum(Ra_results_mode)/len(Ra_results_mode)

    print()
    print("Average_slope (degree)=",Final_Av_slope_from_mode)
    print("Ra (unit length)=",Final_Ra_from_mode)
    print()

    f2.write("\nBest fitting Date and Time: "+str(datetime.now())+"\nNo. of Trials="+str(Trials)+"\ts_range:"+str(s_range)+"\n"+'(s_b,h_b)Mode='+str([round(mode[0],3),round(mode[1],3)])+
            "\t SD_mode="+str(round(MAD_mode,5))+"\n (s_b,h_b)Mean="+str([round(mean[0],4),round(mean[1],5)])+"\t SD_mean="+str(round(SD,6))+"\n"
            +"Av_slope="+str(round(Final_Av_slope_from_mode,3))+"\t Ra="+str(round(Final_Ra_from_mode,6)))

 
    print(f"Time taken={(time.time()-start_time)/60} minutes")

    if (round(mode[0],4)==0.01):
        answer2=input("\nThe Mode value of 's' is marginal. Would you like to check the other range (Y/N)?")
        if answer2=="Y" or answer2=="y":
            if s_range==1:
                s_range=2
                print("Restarting with s_range2")
            elif s_range==2:
                s_range=1
                print("Restarting with s_range1")
        else:
            break
    else:
        break
f2.close()

x_axis=surface.x
y_axis=surface.y
for i in range(len(x_axis)):
    f3.write(str(x_axis[i])+","+str(y_axis[i])+"\n")
f3.close()
print("\nProfile data saved at 'profile.csv'")
x_axis=np.array(x_axis)
y_axis=np.array(y_axis)

if (round(mode[0],4)==0.001):
    print("\nThe mode value of 's' touches the range minimum. It is recommended that you choose a shorter length profile (i.e. less profile divisions) in the shadow pattern image and redo the process.")
if (round(mode[1],3)==0.01):
    print("\nThe mode value of 'h' touches the range maximum. It is recommended that you choose a larger length profile (i.e. more profile divisions) in the shadow pattern image and redo the process.")
elif(round(mode[1],4)==0.001):
    print("\nThe mode value of 'h' touches the range minimum. It is recommended that you choose a shorter length profile (i.e. less profile divisions) in the shadow pattern image and redo the process.")

plt.figure(figsize=(6,6))
plt.title("Equivalent roughness profile (single division)")
plt.xlabel("x")
plt.xlim(0,1/divisions)
plt.ylim(-1/(2*divisions),1/(2*divisions))
plt.ylabel("y(x)")
plt.plot(x_axis,y_axis)
plt.show()


print("Exiting...")
