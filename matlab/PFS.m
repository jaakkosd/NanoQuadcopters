clear

gx = 0; % Goal x-coordinate
gy = 2; % Goal y-coordinate	
R = 1; % Range when avoidance is activated
r = 0.5; % Safe distance
O = [0.01 0; 0.5 0.8];
xO1 = 0.7;
yO1 = 0.8;
xO = -0.01; % Obstacle x-coordinate
yO = 0; % Obstacle y-coordinate
tolerance = 0.10; % When dist between goal and agent is less than tolerance, goal is reached

sim('pFSimulator.slx', 60)

t = readtable('PATH TO YOUR POSFILE');

data = ans;
%sim = plot(data.x.data, data.y.data);
axis equal
hold on
%real = plot(t.x, t.y,'g-', 'LineWidth', 0.5);
s = plot(0.17,-2.4, 'b*');
g = plot(gx,gy, 'black*');

o1 = plot(xO1,yO1, 'r*');
th = 0:pi/50:2*pi;
xunit = R * cos(th) + xO1;
yunit = R * sin(th) + yO1;
R1plot = plot(xunit, yunit);

xunit = r * cos(th) + xO1;
yunit = r * sin(th) + yO1;
r2plot = plot(xunit, yunit);

o = plot(xO,yO, 'r*');
th = 0:pi/50:2*pi;
xunit = R * cos(th) + xO;
yunit = R * sin(th) + yO;
Rplot = plot(xunit, yunit);

xunit = r * cos(th) + xO;
yunit = r * sin(th) + yO;
rplot = plot(xunit, yunit);

xunit = tolerance * cos(th) + gx;
yunit = tolerance * sin(th) + gy;
goalplot = plot(xunit, yunit);

sim = plot(data.x.data, data.y.data, 'Color','b');
real = animatedline('Color','g');

for k = 1:length(t.x)
    addpoints(real,t.x(k),t.y(k));
    drawnow
end

legend([sim real goalplot Rplot rplot o s g],{'sim', 'real', 'tolerance', 'R','r','obstacle', 'start', 'goal'})
hold off