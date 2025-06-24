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

from matplotlib import pyplot as plt
import numpy as np
import random

class SurfaceCurve:
    def __init__(self, scale_factor, height, m_lr, length=1):
        self.scale_factor = scale_factor
        self.height = height
        self.m_lr=m_lr
        self.length = length
        

        self.x = []
        self.y = []
        self.mc = []
        self.A = 0  # Incremental area enclosed at the line by the curve
        self.L = 0  # Incremental length of the straight line
        self.l = 0  # Step for increment

        self._generate_curve()
        self.Ra = self.A / self.length

    def _generate_curve(self):
        """Generates the curve using random values."""
        while self.L < self.length:
            self.x.append(self.L)
            self.y.append(random.choice([-1, 1]) * random.uniform(0, self.height))
            self.l = random.uniform(0, self.scale_factor)
            self.L += self.l

        self.x.append(self.length)  # includes the last value
        self.y.append(random.choice([-1, 1]) * random.uniform(0, self.height))  # includes the last value

        self.x = np.array(self.x)

        for i in range(len(self.x)-1):
            self.mc.append(self.lineParams([self.x[i], self.y[i]], [self.x[i+1], self.y[i+1]]))
            self.A += self.area(self.y[i], self.y[i+1], self.x[i+1]-self.x[i])

    def area(self, y1, y2, l): 
        """Calculates the area between two points."""
        if y1 * y2 > 0:
            return (l / 2) * abs(y1 + y2)
        else:
            return (l / 2) * ((y1**2 + y2**2) / (abs(y1) + abs(y2)))

    def lineParams(self, point1, point2):
        """Calculates the slope (m) and intercept (c) for a line segment."""
        m = (point2[1] - point1[1]) / (point2[0] - point1[0])
        c = point1[1] - m * point1[0]
        return [m, c]

    def y_value(self, m, c, x):
        """Calculates the y value for a given x on a line."""
        return m * x + c

    def calculate_shadow_pattern(self):
        """Calculates the shadow pattern for the curve."""
        #self.m_lr = 0.01  # Slope of the light ray
        Shadow_pattern = []
        k = len(self.y)

        for i in reversed(range(1, len(self.y))):
            flag = False
            if i <= k:
                c_lr = self.y[i] - self.m_lr * self.x[i]
                mc_lr = [self.m_lr, c_lr]

                if not (self.mc[i-1][0] < 0 or self.mc[i-1][0] <= self.m_lr):  # Skipping no-shadow cases
                    l_shadow = 0
                    for j in reversed(range(0, i)):
                        if self.y_value(self.m_lr, c_lr, self.x[j]) > self.y[j]:
                            l_shadow += self.x[j+1] - self.x[j]
                            if j == 0:
                                l_shadow = self.x[i]
                                Shadow_pattern.append([i, l_shadow])
                                #plt.plot([self.x[i], self.x[i] + 0.1], [self.y[i], self.m_lr * (self.x[i] + 0.1) + c_lr], color='red', linestyle='--')
                                flag = True
                                break
                        else:
                            M = np.array([[mc_lr[0], -1], [self.mc[j][0], -1]])
                            C = np.array([-mc_lr[1], -self.mc[j][1]])
                            B = np.linalg.solve(M, C)
                            if B[0] > 0:
                                l_shadow += self.x[j+1] - B[0]
                            else:
                                l_shadow += self.x[j+1]
                                k = 0
                                B[0] = 0
                            k = j
                            Shadow_pattern.append([i, l_shadow])
                            #plt.plot([self.x[i], self.x[i] + 0.1], [self.y[i], self.m_lr * (self.x[i] + 0.1) + c_lr], color='red', linestyle='--')
                            break
            if flag:
                break
        Shadow_pattern_x=[]
        for item in Shadow_pattern:
            #plt.plot([self.x[item[0]], self.x[item[0]]-item[1]], [-0.001, -0.001], color='brown', linewidth=2)
            Shadow_pattern_x.append([self.x[item[0]],item[1]])
        #print("Shadow_pattern_x=",Shadow_pattern_x)

        return Shadow_pattern_x

    def calculate_average_slope(self):
        """Calculates the average slope of the curve."""
        Slope = 0
        for val in self.mc:
            Slope += np.degrees(np.arctan(abs(val[0])))

        return Slope / len(self.mc)

    def plot_curve(self):
        """Plots the curve and shadow patterns."""
        plt.ylim(-0.01, 0.01)
        plt.plot([0, 1.1], [0, 0], color='black', linestyle='--')
        plt.plot(self.x, self.y)
        plt.show()

    def display_info(self):
        """Displays the curve information."""
        print(f'scale_factor={self.scale_factor}, height={self.height}, Ra={self.Ra}, Av_Slope={self.calculate_average_slope()} degrees')
        print('x=', list(self.x))
        print('y=', self.y)
    
    def x_image(self):
        return self.x
    
    def y_image(self):
        return self.y


# Example usage
'''surface = SurfaceCurve(scale_factor=0.05, height=0.01)
surface.calculate_shadow_pattern()
surface.display_info()
surface.plot_curve()'''
