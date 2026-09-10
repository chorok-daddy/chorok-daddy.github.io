%[text] # 제어공학1 2주차 실습 — 물리 모델과 응답
%[text] **자료 버전: 2026-2-02**
%[text] 이 문서는 R2025a 이상의 Live Editor에서 설명과 코드를 함께 보는 실습 문서입니다. 블로그의 MATLAB Online 실습 시작 버튼으로 이 문서를 열고, 본인 작업 공간에서 실행·저장하세요.
%[text] 이 Live Script는 개편된 실습 교재 원본입니다. 본인 사본에서 실행하고 관찰을 기록합니다.
%[text] 이번 실습의 순서는 **예측 → 실행 → 관찰 → 물리적으로 설명**입니다. 회로/기계 모델의 식은 자습 HTML에서 확인하세요. 작성란의 빈 내용을 자신의 말로 채웁니다.
%[text] 특정 제출 파일명/형식은 이 문서에서 새로 정하지 않습니다. 조교와 현재 과제 안내를 따르세요.
%[text] [현재 실습 안내](https://chorok-daddy.github.io/courses/control-1/physical-models/assignment.html)
%% 실행 환경 확인
%[text] ## 0. 먼저 확인하기
%[text] 아래 코드는 MATLAB 버전을 표시하고 필요한 함수를 확인합니다. **Control System Toolbox**가 필요합니다. tf를 찾을 수 없다면 조교에게 환경 확인을 요청하세요.
disp(version);
assert(exist('tf','file') ~= 0, 'Control System Toolbox의 tf 함수를 확인하세요.');
%% RLC 기준 실행
%[text] ## 1. 병렬 RLC의 기준 응답
%[text] 입력은 전류[A], 출력은 전압[V]입니다. 영 초기조건에서 전달함수는 분자 s, 분모 C*s^2 + (1/R)*s + 1/L입니다.
%[text] **실행 전 예상:** 전압은 처음과 오래 후에 어떤 값이 될까요? 작성: ______
R0 = 0.5; % ohm
L0 = 1;   % H
C0 = 5;   % F
t_rlc = linspace(0,25,1001);
g0 = tf([1 0], [C0 1/R0 1/L0]);
disp(g0);
figure('Name','RLC baseline');
step(g0,t_rlc);
grid on;
title('Parallel RLC: 1 A current step');
xlabel('Time (s)'); ylabel('Voltage (V)');
%[text] **관찰:** 예상과 같은 점/다른 점을 적으세요. 작성: ______
%[text] 계수 배열은 s의 높은 차수부터 적습니다. 분자 [1 0]의 마지막 0을 생략하면 다른 모델이 됩니다.
%% RLC 한 변수씩 변경
%[text] ## 2. R, L, C를 한 가지씩 바꾸기
%[text] 아래에서 parameter를 "R", "L", "C" 중 하나로, factor를 2 또는 0.5로 바꾸고 이 섹션을 실행하세요. 기준 모델은 그대로 유지되어 두 곡선을 비교할 수 있습니다.
%[text] 처음에는 factor=1이므로 두 곡선이 겹칩니다. 코드를 이해한 뒤 값을 바꾸세요. 각 파라미터의 2배/0.5배 등 변화를 비교해 기록합니다.
parameter = "R"; % 학생이 바꿀 부분: "R", "L", "C"
factor = 1;      % 학생이 바꿀 부분: 2 또는 0.5
assert(any(parameter == ["R","L","C"]), 'parameter는 R, L, C 중 하나여야 합니다.');
assert(isscalar(factor) && isfinite(factor) && factor > 0, 'factor는 양수여야 합니다.');
R = R0; L = L0; C = C0;
switch parameter
    case "R"
        R = R0*factor;
    case "L"
        L = L0*factor;
    case "C"
        C = C0*factor;
end
g_changed = tf([1 0], [C 1/R 1/L]);
figure('Name','RLC comparison');
step(g0,g_changed,t_rlc);
grid on;
legend('Baseline',char(parameter + " x " + string(factor)), 'Location','best');
title('Change one parameter');
xlabel('Time (s)'); ylabel('Voltage (V)');
%[text] 아래는 관찰을 정리할 표입니다. 각 행에 해당하는 실험을 수행한 뒤 채우세요. 그래프를 저장한다면 어떤 파라미터 값인지 표시하세요.
%[text:table]
%[text] | 변경 | 실행 전 예상 | 그래프 관찰 | 물리적 설명 |
%[text] | --- | --- | --- | --- |
%[text] | R x 2 | 미작성 | 미작성 | 미작성 |
%[text] | R x 0.5 | 미작성 | 미작성 | 미작성 |
%[text] | L x 2 | 미작성 | 미작성 | 미작성 |
%[text] | L x 0.5 | 미작성 | 미작성 | 미작성 |
%[text] | C x 2 | 미작성 | 미작성 | 미작성 |
%[text] | C x 0.5 | 미작성 | 미작성 | 미작성 |
%[text:table]
%[text] **해석 힌트:** 무엇이 변하고 무엇이 유지되는지 나누어 보세요. 저항의 영향은 오늘의 병렬 회로에서 생각해야 합니다.
%% 기계 시스템 기준 실행
%[text] ## 3. 질량–스프링–댐퍼의 기준 응답
%[text] 입력은 힘[N], 출력은 평형점 기준 변위[m]입니다. 식은 M*y'' + b*y' + k*y = u입니다. 분자는 1, 분모 계수는 [M b k]입니다.
%[text] **실행 전 예상:** 일정한 힘을 계속 가하면 변위가 계속 커질까요? 작성: ______
M = 1; b = 2; k = 5;
t_msd = linspace(0,15,1001);
g_msd = tf(1,[M b k]);
figure('Name','Mechanical baseline');
step(g_msd,t_msd);
grid on;
title('Mass-spring-damper: 1 N force step');
xlabel('Time (s)'); ylabel('Displacement (m)');
%[text] **관찰과 이유:** 작성: ______
%% 기계 시스템 세 경우 비교
%[text] ## 4. 세 경우를 한 그래프에서 비교하기
%[text] 원문 과제의 세 경우: 기본 [1 2 5], 댐핑 증가 [1 8 5], 스프링 증가 [1 2 10]. 각 행의 순서는 [M b k]입니다.
%[text] 아래는 아직 세 행이 모두 기본값인 시작 코드입니다. **두 번째와 세 번째 행을 과제 조건에 맞게 바꾸세요.** 처음 실행해서 선이 겹치는 것은 이 때문입니다.
cases = [1 2 5;
         1 2 5;  % 학생이 바꿀 부분: 댐핑 증가 조건
         1 2 5]; % 학생이 바꿀 부분: 스프링 증가 조건
assert(isequal(size(cases),[3 3]) && all(cases(:)>0), 'cases는 양수의 3x3 배열이어야 합니다.');
figure('Name','Mechanical comparison');
hold on;
for idx = 1:3
    g_case = tf(1,cases(idx,:));
    [y_case,time_case] = step(g_case,t_msd);
    plot(time_case,y_case,'LineWidth',1.5);
end
hold off;
grid on;
legend('Case 1','Case 2','Case 3','Location','best');
title('Compare the three cases');
xlabel('Time (s)'); ylabel('Displacement (m)');
%[text:table]
%[text] | 경우 | 최종값에 관한 관찰 | 진동/피크에 관한 관찰 | 안정되는 시간에 관한 관찰 |
%[text] | --- | --- | --- | --- |
%[text] | Case 1 | 미작성 | 미작성 | 미작성 |
%[text] | Case 2 | 미작성 | 미작성 | 미작성 |
%[text] | Case 3 | 미작성 | 미작성 | 미작성 |
%[text:table]
%[text] **설명:** 댐핑을 키우는 것과 빨리 안정되는 것은 같은 뜻일까요? 스프링을 키웠을 때 최종값도 같은가요? 그래프와 모델식에 근거해 적으세요. 작성: ______
%% 마지막 확인
%[text] ## 5. 저장·제출 전 확인
%[text] - RLC에서 각 파라미터 변경 결과와 물리적 의미를 기록했는가?
%[text] - 기계 모델의 두 번째/세 번째 행을 실제 과제 조건으로 수정했는가?
%[text] - 세 경우가 한 그래프에 표시되고 범례·단위를 읽을 수 있는가?
%[text] - 미작성/빈칸을 채우고 결과를 자신의 말로 설명했는가?
%[text] - 본인 작업이 저장되어 있고 제출 방식은 조교 안내와 일치하는가? \
%[text] 현재 확인된 KLAS 2주차 과제 마감: 2026-09-10 23:59. 변경되면 최신 공지를 따르세요.
%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"inline","rightPanelPercent":40}
%---
