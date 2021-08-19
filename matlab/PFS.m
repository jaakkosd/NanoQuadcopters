clear

% CF1 starting coords:
sx1 = -0.30; 
sy1 = 2.03;

% CF2 starting coords:
sx2 = 0.11;
sy2 = -2.07;

gx1 = 0; % Goal x-coordinate
gy1 = -2; % Goal y-coordinate
gx2 = 0; % Goal x-coordinate
gy2 = 2; % Goal y-coordinate	
tolerance = 0.10; % When dist between goal and agent is less than tolerance, goal is reached

sim('pFSimulator.slx', 60)

t1 = readtable('YOUR PATH TO pos1.csv FILE');
t3 = readtable('YOUR PATH TO pos3.csv FILE');

data = ans;
sim2 = plot(data.x1.data, data.y1.data, 'g');
hold on
sim1 = plot(data.x2.data, data.y2.data, 'r');
axis equal

th = 0:pi/50:2*pi;
plotgx1 = tolerance * cos(th) + gx1;
plotgy1 = tolerance * sin(th) + gy1;
goalplot1 = plot(plotgx1, plotgy1, 'g');

plotgx2 = tolerance * cos(th) + gx2;
plotgy2 = tolerance * sin(th) + gy2;
goalplot2 = plot(plotgx2, plotgy2, 'r');

real1 = animatedline('Color','r', 'LineStyle', '--');
real3 = animatedline('Color','g', 'LineStyle', '--');

plot(sx1, sy1, 'Color', 'g', 'Marker', 'x')
plot(sx2, sy2, 'Color', 'r', 'Marker', 'x')

l1 = length(t1.x1);
l3 = length(t3.x3);

l = max([l1 l3]);

for k = 1:l
    
    if k < length(t1.x1)
        addpoints(real1,t1.x1(k),t1.y1(k));
    end
    
    if k < length(t3.x3)
        addpoints(real3,t3.x3(k),t3.y3(k));
    end
    
    drawnow
    pause(0.01)
end

legend([sim1 sim2 real1 real3],{'CF1sim', 'CF3sim', 'CF1', 'CF3'})
hold off