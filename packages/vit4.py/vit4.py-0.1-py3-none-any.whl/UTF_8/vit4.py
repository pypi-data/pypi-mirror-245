x=input().lower()
pas = '''a = 1
while length(a) < 10
a = [a 0]+ [0 a]
plot(a)
end
#Matrix operation
A=[1 2;3 4]
B=[4 5;8 12]
C=A+B
D=A*B
E=inv(A)
F=B'
H=A.^2
I= det(A)

'''

crcl ='''

#2.Circle with centre(1,3)
t = linspace(0, 2*pi, 101);
x = 1 +2*cos(t);
y = 3 +2*sin(t);
plot(x,y)
axis equal

'''

plot3 ='''

%3.plotting three functions without hold on
x = linspace(0,1,101)
plot(x,x.^3,'r+',x,sin(x),'b-',x,exp(x),'g.')

%5.solve 4x+5y=7,7x+8y=21
A=[4 5;7 8]
b=[7 21]'
x=A\b

'''

quadeq ='''


%6.solving quadratic equations
solve('2*x^2+5*x+12')

%7subplot
x=0:.1:2*pi;
subplot(2,2,1);
plot(x,sin(x));
subplot(2,2,2);
plot(x,cos(x));
subplot(2,2,3)
plot(x,exp(-x));
subplot(2,2,4)

'''
symdiff ='''
%8.symbolic differentiation
syms x y
f =x^2+2*x*y+y*sin(x)
diff(f,x)
diff(f,y)

'''
symint = '''

%9.Symbolic integration
f=x^3+3*x^2+5*x+12
int(f,x,0,2)
'''

ezplot ='''
%10.ezplotting
syms x
f=sin(2*x)+cos(3*x)
ezplot(f)

'''
crclplot ='''
+++++++++++++(1) To Plot the Circle
clc
clear all
syms r a b
r= input('Enter the radius of the circle')
a= input('Enter the x coordinate of the center')
b= input('Enter the y coordinates of the center')
t = linspace(0, 2*pi, 100);
x = a+r*cos(t);
y = b+r*sin(t);
axis equal
plot(x,y)
xlabel('x-Coordinate')
ylabel('x-Coordinate')
title('(x—a)^2 + (y—b)^2 = r^2')
'''

hold='''
+++++++++(2) Multiple plots using Hold on Matlab Code
clc
clear all
x = linspace(0, 1, 100);
plot(x, x^2,'r', 'LineWidth',2.0)
hold on
plot(x, cos(x), 'g', 'LineWidth',2.0)
hold on
plot(x,sin(x),'b','LineWidth',2.0)
hold on
plot(x,exp(x),'c','LineWidth',2.0)
legend('x^2','cos(x)','sin(x)','e^x')

'''

donothold ='''
+++++++++++(3) Multiple plots without command "hold on" Matlab Code
clc
clear all
x = linspace(0,1, 200);
plot( x, sin(x),x, cos(x), x, x.^3, x, tan(x), 'LineWidth',2.0)
legend('sin(x)','cos(x)', 'x^3' , 'tan(x)') 
'''

subplot='''

++++++++++++(4) Multiple plots using
Matlab Code
clc
Clear all
x=0:0.1:2*pi;
subplot(2,2,1)
plot(x,sin(x));
title('sin(x)') subplot (2,2,2)
plot(x,cos(x), 'r-*');
title('cos(x)') subplot(2,2,3)
plot(x,exp(-x),'go')
title('e^-x') subplot(2,2,4);
plot(x,sin(3 * x), 'ms')
title('sin(3x)')

'''

crvez='''
++++++++++++(5) Graph of the curve using ezplot
Matlab Code
clc
clear all
syms x
f=sin(2*x)+cos(3*x)
figure(1)
ezplot(f)
figure(2)
ezplot(f,[0,3])
''',

crvtgt='''

++++++++++++(6) Graph of a curve and its tangent line in the neighbourhood D of a point.
Matlab Code
clc
clear all
syms x
y=input('enter a function f in terms of x:')
x1=input('enter x value at which tangent:')
D = [x1-2 x1+2]
ezplot(y,D)
hold on
yd = diff(y,x);
slope = subs(y,x,x1)
y1 = subs(y,x,x1);
plot(x1,y1,'ko')
tgtline = slope*(x-x1)+y1
'''

deriv='''
++++++++++++(1) To Plot the function and its derivatives
Matlab Code
clc
clear all
syms x real
f= input ('Enter the function f(x):');
fx= diff(f,x)
fxx= diff(fx,x)
D = [0,5];
l=ezplot(f,D)
set(1,'color','b');
hold on
l=ezplot(fx,D);
set(l,'color','r');
h=ezplot (fxx,D);
set(h,'color','g');
legend('f','fx','fxx')
legend('Location','northeastoutside')

'''
mnmx1='''
++++++++++(2) To find the maxima and minima of the single variable function and visu-
alize it.
Matlab Code
clc
clear all
syms x real
f= input ('Enter the function f(x):');
fx= diff(f,x);
fxx= diff(fx,x);
c= solve(fx)
c=double(c);
for i = 1:length(c)
T1 = subs(fxx, x ,c(i) );
T1=double(T1);
T3= subs(f, x, c(i));
T3=double(T3);
if (T1==0)
sprintf('The inflection point is x = %d',c(i))
else
if (T1 < 0)
sprintf('The maximum point x is %d', c(i))
sprintf('The maximum value of the function is %d', T3)
else
sprintf('The minimum point x is %d', c(i))
sprintf('The minimum value of the function is %d', T3)
end
end
cmin = min(c);
cmax = max(c);
D = [cmin-2, cmax+2]; 
ezplot(f,D)
hold on
plot(c(i), T3, 'g*', 'markersize', 15);
end 
'''
aicrv='''
++++++++++(3) To find the area of the regions enclosed by curves and visualize it.
Matlab Code
clc
clear
syms x
y1=input('ENTER the upper curve as a function of x: ');
y2=input('ENTER the lower curve as a function of x:' );
t=solve(y1-y2);
t=double(t);
A=int(y1-y2, t(1), t(2))
D=[t(1)-0.2 t(2)+0.2];
ez1=ezplot (y1,D);
set(ez1,'color','r')
hold on
ez2=ezplot(y2, D);
set(ez2,'color','g')
xv = linspace(t(1),t(2));
y1v =subs(y1,x,xv);
y2v = subs(y2,x,xv);
x= [xv,xv];
y= [y1v,y2v];
fill (x,y,'b')
'''


srev='''
+++++++++++++++%volume of solid of revolution
clc
clear all
syms x
f=input('Enter the function: ');
fL=input('Enter the interval on which the function is defined: ');
yr =input('Enter the axis of rotation y = c (enter only c value): ');
iL=input('Enter the integration limits: ');
Volume = pi*int((f-yr)^2, iL(1), iL(2));
disp(['Volume is: ', num2str(double(Volume))])
fx = inline(vectorize(f));
xvals=  linspace (fL(1),fL(2),201);
xvalsr= fliplr(xvals);
xivals = linspace(iL(1),iL(2),201);
xivalsr= fliplr(xivals);
xlim = [fL(1) fL(2)+0.5];
ylim = fx(xlim);
figure('Position', [100 200 560 420])
subplot(2,1,1)
hold on;
plot(xvals,fx(xvals),'-b','LineWidth',2); 
[X,Y,Z]= cylinder (fx(xivals)-yr, 100);
figure('Position', [700 200 560 420])
Z = iL(1) + Z.*(iL(2)-iL(1));
surf(Z,Y+yr, X, 'EdgeColor', 'none', 'FaceColor', 'flat', 'FaceAlpha',0.6);
hold on;
plot([iL(1) iL(2)],[yr yr], '-r', 'LineWidth', 2);
axis equal;
xlabel('X-axis');
ylabel('Y-axis');
zlabel('Z-axis');
view(22,11);

'''


mnmx2='''
++++++++++++++++%maxima and minima of two variable function
clc 
clear 
syms x y 
f(x,y)=input('Enter the function f(x,y):'); 
p=diff(f,x); q=diff(f,y); 
[ax,ay]=solve(p,q); 
ax=double(ax);ay=double(ay); 
r=diff(p,x); s=diff(p,y); t=diff(q,y);D=r*t-s^2; 
figure 
fsurf(f); 
legstr={'Function Plot'};% for Legend
for i=1:size(ax) 
T1=D(ax(i),ay(i)); 
T2=r(ax(i),ay(i)); 
T3=f(ax(i),ay(i)); 
if(double(T1)==0) 
sprintf('At (%f,%f) further investigation is required',ax(i),ay(i)) 
legstr=[legstr,{'Case of Further investigation'}]; 
mkr='ko'; 
elseif (double(T1)<0) 
sprintf('The point (%f,%f) is a saddle point', ax(i),ay(i)) 
legstr=[legstr,{'Saddle Point'}]; % updating Legend
mkr='bv'; % marker
else
if (double(T2) < 0) 
sprintf('The maximum value of the function is f(%f,%f)=%f', ax(i),ay(i), T3) 
legstr=[legstr,{'Maximum value of the function'}];% updating Legend
mkr='g+';% marker
else
sprintf('The minimum value of the function is f(%f,%f)=%f', ax(i),ay(i), T3) 
legstr=[legstr,{'Minimum value of the function'}];% updating Legend 
mkr='r*'; % marker
end
end
hold on
plot3(ax(i),ay(i),T3,mkr,'Linewidth',4); 
end
legend(legstr,'Location','Best');
'''

lng2='''

++++++++++++++++%MatLab code for Lagrange's multiplier method for two variables:

clc
clearvars
syms x y L
f = input('Enter the function f(x,y): ');
g = input('Enter the constraint function g(x,y): ');
F = f + L*g;
gradF = jacobian(F, [x, y]);
[L,x1,y1] = solve(g,gradF(1),gradF(2),'Real',true); % Solving only for Real x and y
x1 = double(x1); y1 = double (y1);
xmx = max(x1); xmn = min(x1); % Finding max and min of x-coordinates for plot range
ymx = max(y1); ymn = min (y1); % Finding max and min of y-coordinates for plot range
range = [xmn-3 xmx+3 ymn-3 ymx+3]; % Setting plot range
ezmesh(f,range);hold on;grid on;
h = ezplot(g, range); set(h, 'LineWidth', 2);
tmp = get(h,'contourMatrix');
xdt = tmp(1,2:end); % Avoiding first x-data point
ydt = tmp(2,2:end); % Avoiding first y-data point.
zdt = double(subs(f,{x,y},{xdt,ydt}));
plot3(xdt,ydt,zdt,'-r','LineWidth',2);axis(range);
for i = 1:numel(x1)
   G(i) = subs(f, [x, y], [x1(i),y(i)])
   plot3(x1(i),y1(i),G(i),'*k','MarkerSize',20);
end
title('Constrained Maxima/Minima')

'''


lng3='''

+++++++++++MatLab code for Lagrange's multiplier method for three variables:
clc
clear vars
syms x y z L
f= input('Enter the function f(x, y, z):');
g= input('Enter the constraint function g(x,y,z):');
F = f + L*g;
gradF= jacobian(F, [x, y, z]);
[L,x1,y1,z1] = solve(g,gradF(1) ,gradF(2) ,gradF(3));
Z=[x1 y1 z1];
disp('[x y z]=')
disp(Z)

'''

li='''
+++++++++++MatLab code for line integral

clc 
clear 
syms t x y 
f=input('enter the f vector as i and j order in vector form:'); 
rbar = input('enter the r vector as i and j order in vector form:'); 
lim=input('enter the limit of integration:'); 
vecfi=input('enter the vector field range'); % knowledge of the curve is essential 
drbar=diff(rbar,t); 
sub = subs(f,[x,y],rbar); 
f1=dot(sub,drbar) 
int(f1,t,lim(1),lim(2)) 
P = inline(vectorize(f(1)), 'x', 'y'); 
Q = inline(vectorize(f(2)), 'x', 'y') 
x = linspace(vecfi(1),vecfi(2), 10); y = x; 
[X,Y] = meshgrid(x,y); 
U = P(X,Y); 
V = Q(X,Y); 
quiver(X,Y,U,V) 
hold on
fplot(rbar(1),rbar(2),[lim(1),lim(2)]) 
axis on
xlabel('x') 
ylabel('y') 

'''

grn='''
+++++++++++++++++Matlab code for green's theorem

clc 
clear all
syms x y r t
F=input('enter the F vector as i and j order in vector form:'); 
integrand=diff(F(2),x)-diff(F(1),y); 
polarint=r*subs(integrand,[x,y],[r*cos(t),r*sin(t)]); 
sol=int(int(polarint,r,0,3),t,0,2*pi); 
P = inline(vectorize(F(1)), 'x', 'y'); 
Q = inline(vectorize(F(2)), 'x', 'y') 
x = linspace(-3.2,3.2, 10); y = x; 
[X,Y] = meshgrid(x,y); 
U = P(X,Y); 
V = Q(X,Y); 
quiver(X,Y,U,V) 
hold on
fplot(3*cos(t),3*sin(t),[0,2*pi]) 
axis equal

''',

vf2d='''

+++++++++++++++Matlab code for drawing 2d vector field

clc 
clear all 
syms x y 
F=input( 'enter the vector as i, and j order in vector form:'); 
P = inline(vectorize(F(1)), 'x', 'y'); 
Q = inline(vectorize(F(2)), 'x', 'y'); 
x = linspace(-1, 1, 10); 
y = x; 
[X,Y] = meshgrid(x,y); 
U = P(X,Y); 
V = Q(X,Y); 
quiver(X,Y,U,V,1) 
axis on
xlabel('x') 
ylabel('y') 

'''
vf3d='''
+++++++++++++Matlab code for drawing 3d vector field

clc
clear all
syms x y z 
F=input( 'enter the vector as i,j and k order in vector form:') 
P = inline(vectorize(F(1)), 'x', 'y','z'); 
Q = inline(vectorize(F(2)), 'x', 'y','z'); 
R = inline(vectorize(F(3)), 'x', 'y','z'); 
x = linspace(-1, 1, 5); y = x; 
z=x; 
[X,Y,Z] = meshgrid(x,y,z); 
U = P(X,Y,Z); 
V = Q(X,Y,Z); 
W = R(X,Y,Z); 
quiver3(X,Y,Z,U,V,W,1.5) 
axis on
xlabel('x') 
ylabel('y') 
zlabel('z')
'''

grad='''
+++++++++++++++Matlab code gradient and draw grad vector field


clc 
clear all 
syms x y
f=input( 'enter the function f(x,y):'); 
F=gradient(f) 
P = inline(vectorize(F(1)), 'x', 'y'); 
Q = inline(vectorize(F(2)), 'x','y'); 
x = linspace(-2, 2, 10); 
y = x; 
[X,Y] = meshgrid(x,y); 
U = P(X,Y); 
V = Q(X,Y); 
quiver(X,Y,U,V,1) 
axis on xlabel('x') 
ylabel('y') 
hold on
ezcontour(f,[-2 2]) 
'''

dc ='''
+++++++++++++++++Matlab code for curl and divergenge

clc 
clear all
syms x y z real 
F=input( 'enter the vector as i, j and k order in vector form:') 
curl_F = curl(F, [x y z]) 
div_F = divergence(F, [x y z])
'''

vcf ='''

++++++++++++++++Determine whether or not the vector field is conservative. If it is
conservative, find a function f such that .

clc 
clear all
syms x y z real
F=input( 'enter the vector as i,j and k order in vector form:') 
curl_F = curl(F, [x y z]) 
if (curl_F ==[0 0 0]) 
 f = potential(F, [x y z]) 
else
 sprintf('curl_F is not equal to zero') 
end


'''

auc = '''
+++++++++++++Matlab code for area under curve

clc
clear
syms x
y1=input('ENTER the upper curve as a function of x : ');
y2=input('ENTER the lower curve as a function of x : ');
% Try the curves : y=x and y=x^2-2*x;
t=solve(y1-y2)
t=double(t);

A=int(y1-y2,t(1),t(2))
D=[t(1)-0.2 t(2)+0.2];
ez1=ezplot(y1,D);
set(ez1,'color','r')
hold on
ez2=ezplot(y2,D);
set(ez2,'color','g')
xv = linspace(t(1),t(2));
y1v =subs(y1,x,xv); 

y2v = subs(y2,x,xv);
x = [xv,xv];
y = [y1v,y2v];
fill(x,y,'b')
'''


vgrn='''

++++++++++++++Matlab code for verification of green's theorem


clc
clear
syms x
y1=input('ENTER the upper curve as a function of x : ');
y2=input('ENTER the lower curve as a function of x : ');
% Try the curves : y=x and y=x^2-2*x;
t=solve(y1-y2)
t=double(t);

A=int(y1-y2,t(1),t(2))
D=[t(1)-0.2 t(2)+0.2];
ez1=ezplot(y1,D);
set(ez1,'color','r')
hold on
ez2=ezplot(y2,D);
set(ez2,'color','g')
xv = linspace(t(1),t(2));
y1v =subs(y1,x,xv); 

y2v = subs(y2,x,xv);
x = [xv,xv];
y = [y1v,y2v];
fill(x,y,'b')

'''
D={'pas':pas,'crcl':crcl,'plot3':plot3,'quadeq':quadeq,'symdiff':symdiff,'symint':symint,'ezplot':ezplot,'crclplot':crclplot,'hold':hold,'donothold':donothold,'subplot':subplot,'crvez':crvez,'crvtgt':crvtgt,'deriv':deriv,'mnmx1':mnmx1,'aicrv':aicrv,'srev':srev,'mnmx2':mnmx2,
   'lng2':lng2,'lng3':lng3,'li':li,'grn':grn,'vf2d':vf2d,'vf3d':vf3d,'grad':grad,'dc':dc,'vcf':vcf,'auc':auc,'vgrn':vgrn}
try :
    import pyperclip as pp 
    pp.copy(D[x])
except Exception as e :
    print(D[x])