x=input().lower()
diff='''    clc
    clear all
    syms x
    f=input('enter the function of x')
    fx=diff(f,x)
    fxx=diff(fx,x)
    p=solve(fx)%To find the critical points
    p=double(p)
    for i=1:length(p)
        T1=subs(fxx,x,p(i))
        T1=double(T1)
        T3=subs(f,x,p(i))
        T3=double(T3)
    if (T1==0)
        sprintf('the inflection point is= %d',p(i))
    else
    if (T1<0)
        sprintf('this is the point of maxima=%d',p(i))
        sprintf('the maximum value of the function is =%d',T3)
    else
        sprintf('this is the point of minima=%d',p(i))
        sprintf('the minimum value of the function is =%d',T3)
    end
    end
    pmin=min(p)
    pmax=max(p)
    D=[pmin-2 pmax+2]
    fplot(f,D)
    hold on
    plot(p(i),T3,'g*','MarkerSize',15)'''

integration='''    clc
    clear all
    syms x
    upper_bound=input('enter the upper bound of the funciton in terms of x:')
    lower_bound=input('enter the lower bound of the function in terms of x:')
    t=solve(upper_bound-lower_bound)
    t=double(t)
    A=int(upper_bound-lower_bound,t(1),t(2))
    D=[t(1)-0.2 t(2)+0.2]
    fplot(upper_bound,D)
    hold on
    fplot(lower_bound,D)
    hold on
    h=linspace(t(1),t(2))
    x1=subs(upper_bound,x,h)
    x2=subs(lower_bound,x,h)
    x=[h,h]
    y=[x1,x2]
    fill(x,y,'b')'''
    
vols='''    clc
    clear all
    syms x
    f=input('enter the function')
    fL=input('enter  the range in which funcion is defined')
    yr=input('enter the axis of rotation')
    iL=input('enter the limits of integration')
    volume=pi*int((f-yr)^2,iL(1),iL(2))
    disp(['volume is:',num2str(double(volume))])
    fx=inline(vectorize(f))
    xvals=linspace(fL(1),fL(2),201)
    xvalsr=fliplr(xvals)
    xivals=linspace(iL(1),iL(2),201)
    xivalsr=fliplr(xivals)
    xlim=[fL(1) fL(2)+0.5]
    ylim=fx(xlim)
    figure('Position',[100 200 560 420])
    subplot(2,1,1)
    hold on
    plot(xvals,fx(xvals),'b')
    [X,Y,Z]=cylinder(fx(xivals)-yr,100)
    figure('Position',[700 200 560 420])
    Z=iL(1)+Z.*(iL(2)-iL(1))
    surf(Z,Y+yr,X,'EdgeColor','none','FaceColor','flat','FaceAlpha',0.6)
    hold on
    plot([iL(1) iL(2)],[yr yr],'-r','LineWidth',2)
    xlabel('x-axis');
    ylabel('y-axis');
    zlabel('z-axis');
    view(22,11);'''
    
max_min='''    clc
    clear all
    syms x y
    f=input('enter a function in terms of x and y')
    a=diff(f,x);b=diff(f,y)
    [ax,ay]=solve(a,b)
    r=diff(a,x);s=diff(a,y);t=diff(b,y);D=r*t-s^2;
    fsurf(f)
    for i=1:size(ax)
    T1=D(ax(i),ay(i))
    T2=r(ax(i),ay(i))
    T3=f(ax(i),ay(i))
    if double(T1==0)
    sprintf('(%f,%f) needs further investigation',ax(i),ay(i))
    elseif double(T1<0)
    sprintf('(&f,%f) is a saddle point',ax(i),ay(i))
    else
    if T2>0
    sprintf('f(%f,%f)=%f is maximum value of the funcion',ax(i),ay(i),T3)
    elseif T2<0
    sprintf('f(%f,%f)=%f is the minimum value of the funtion',ax(i),ay(i),T3)
    end
    end
    hold on 
    plot(ax(i),ay(i),T3,mkr,'Linewidth',4)
    end'''

lang='''    clc
    clear all
    syms x y L
    f=input('enter the function');
    g=input('enter the equation of the constraint ');
    F=f+g*L;
    gradF=jacobian(F,[x,y]);
    [L,x1,y1]=solve(g,gradF(1),gradF(2),'Real',true);
    x1=double(x1);y1=double(y1);
    xmax=max(x1);xmin=min(x1);
    ymax=max(y1);ymin=min(y1);
    range=[xmin-3 xmax+3 ymin-3 ymax+3];
    fmesh(f,range);
    hold on;
    grid on;
    h=ezplot(g,range);
    set(h,'linewidth',2)
    tmp=get(h,'contourMatrix');
    xdt=tmp(1,2:end);
    ydt=tmp(2,2:end);
    zdt=double(subs(f,{x,y},{xdt,ydt}));
    plot3(xdt,ydt,zdt,'-r','LineWidth',2)
    axis(range);
    for i=1:numel(x1)
        G=subs(f,[x,y],[x1(i),y1(i)]);
        plot3(x1(i),y1(i),G(i),'*k','MarkerSize',20);
    end
    title('constrained maxima/minima')
    %for three varibles
    clc
    clearvars
    syms x y z L
    f=input('enter the function in x y z')
    g=input('enter the equation of the constraint')
    F=f+g*L
    gradF=jacobian(f,[x,y,z])
    [L,x1,y1,z1] =solve(g,gradF(1),gradf(2),gradF(3))
    disp('[x y z]=')
    disp([x1,y1,z1])'''

views='''    syms x y z
    int(int((x+y)/4,y,x/2,x),x,1,2)
    viewSolid(z,0+0*x+0*y,(x+y)/4,y,x/2,x,x,1,2)'''
D={'diff':diff,'integration':integration,'vols':vols,'max_min':max_min,'lang':lang,'views':views}
try :
    import pyperclip as pp 
    pp.copy(D[x])
except Exception as e :
    print(D[x])