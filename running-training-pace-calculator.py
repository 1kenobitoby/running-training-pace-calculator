import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Running training pace calculator",
    page_icon="media/favicon.ico",
    layout="centered",
    initial_sidebar_state="auto",
    #menu_items={
        #'Get Help': '<<URL>>',
        #'Report a bug': "<<URL>>",
        #'About': "Made with Streamlit v1.27"
    #}
)

# Hack css style to force columns not to respond
st.write('''<style>

    [data-testid="column"] {
        width: calc(33.3333% - 1rem) !important;
        flex: 1 1 calc(33.3333% - 1rem) !important;
        min-width: calc(33% - 1rem) !important;
    }
    </style>''', unsafe_allow_html=True) 

# html strings used to render donate button and link and text
donate_text = '<h6> Useful? Buy us a coffee. </h6>'

html_donate_button = '''
<form action="https://www.paypal.com/donate" method="post" target="_blank">
<input type="hidden" name="hosted_button_id" value="6X8E9CL75SRC2" />
<input type="image" src="https://www.paypalobjects.com/en_GB/i/btn/btn_donate_SM.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button"/>
<img alt="" border="0" src="https://www.paypal.com/en_GB/i/scr/pixel.gif" width="1" height="1" />
</form>
'''   

def redirect_button(url: str):
    st.markdown(
    f"""
    <a href="{url}" target="_blank">
        <div>
        <img src="https://www.paypalobjects.com/en_GB/i/btn/btn_donate_SM.gif" alt="Donate with PayPal button">
        </div>
    </a>
    """,
    unsafe_allow_html=True
    )

st.image('media/logo.png', width=100)
st.title('Running training pace calculator')
   

st.write('This app lets you calculate appropriate running training paces for different running fitness goals. It lets you input a finishing time for a recent distance race to calculate what is known as your \'VDOT\'. Or if you know your VDOT already, you can input that directly. Your VDOT is a measure of how rapidly your body can absorb oxygen from the air, get it to your running muscles and use it to propel you forward. There is a well established relationship between your VDOT and your potential finishing time over a wide range of running race distances. Generally speaking, the higher your VDOT the faster you can run a long distance. Your VDOT also controls how fast your training pace should be to achieve your fitness goals. Here we back calculate your VDOT from a race time and use that to suggest appropriate paces for your running training. If you need a fuller explanation of how all this works, expand the Notes section at the bottom of the page. To get started, either enter a race time or select your known VDOT below.')

st.divider()
st.write('***Either enter a recent race time...***')
distance = st.selectbox('Select your race distance from the dropdown', ('1500m', '1 mile', '3000m', '2 miles','5000m', '10,000m', '15km', 'Half marathon', 'Marathon'), index=None)

st.markdown('<small>And enter your finishing time</small>', unsafe_allow_html=True)
hrs, mins, secs = st.columns(3)
with hrs:
    race_hours = st.number_input('Hours', min_value=0, max_value=6, step=1)

with mins:
    race_mins = st.number_input('Mins', min_value=0, max_value=59, step=1)

with secs:
    race_secs = st.number_input('Secs', min_value=0, max_value=59, step=1, help='Enter your finishing time in hours, minutes and seconds format')

lookup_table = pd.read_csv('vdot_times_distances_secs.csv')
time = race_secs + 60 * race_mins + 3600 * race_hours

#Initialise vdot
vdot = 29

# 'and' binds tighter than 'or' so need parentheses (otherwise you're only entering if race hours not zero AND distance not None)
if (race_secs !=0 or race_mins !=0 or race_hours !=0) and distance is not None:
    #find the closest value to the race time in the distance column
    lookup = lookup_table.iloc[(lookup_table[distance]-time).abs().argsort()[:1]]
    #Produces a 1 row dataframe, get the value (.item()) of the VDOT column
    vdot = lookup['VDOT'].item()

st.write('\n')
st.write('\n')
st.write('***...or use the slider to input your known VDOT***')
trigger = st.slider('Your VDOT', min_value=29, max_value=85, step=1, value=vdot)

st.divider()
if trigger <30:
    st.write('***Enter something above to see your training paces***')
else:
    paces = pd.read_csv('vdot_paces_secs.csv')
    easy_mile = paces.loc[paces['VDOT'] == trigger, 'E_secs/mile'].item()
    easy_km = paces.loc[paces['VDOT'] == trigger, 'E_secs/km'].item()
    m_mile = paces.loc[paces['VDOT'] == trigger, 'M_secs/mile'].item()
    m_km = paces.loc[paces['VDOT'] == trigger, 'M_secs/km'].item()
    t_mile = paces.loc[paces['VDOT'] == trigger, 'T_secs/mile'].item()
    t_km = paces.loc[paces['VDOT'] == trigger, 'T_secs/1000m'].item()
    i_400 = paces.loc[paces['VDOT'] == trigger, 'I_secs/400m'].item()
    i_km = paces.loc[paces['VDOT'] == trigger, 'I_secs/1000m'].item()
    i_mile = paces.loc[paces['VDOT'] == trigger, 'I_secs/mile'].item()
    r_200 = paces.loc[paces['VDOT'] == trigger, 'R_secs/200m'].item()
    r_400 = paces.loc[paces['VDOT'] == trigger, 'R_secs/400m'].item()
    r_800 = paces.loc[paces['VDOT'] == trigger, 'R_secs/800m'].item()

    st.markdown('<h5><em>For a VDOT of <span style="color:#F63366;">' + "%.0f" % trigger + '</span> these are your training paces:</em></h5>', unsafe_allow_html=True)
    st.write('***Your E (easy) running pace is:***')      
    st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % (int(easy_mile/60)) +' minutes and ' + "%.0f" % (easy_mile % 60) + ' seconds per mile</strong></em></span>', unsafe_allow_html=True)
    st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % (int(easy_km/60)) +' minutes and ' + "%.0f" % (easy_km % 60) + ' seconds per km</strong></em></span>', unsafe_allow_html=True)
    st.write('Beginners should spend all their time in this zone for a few weeks at least. Experienced distance athletes should spend over half their time in this zone using it for your warm ups, cool downs, recovery periods between fast repetitions and the long Sunday run. Develops most of the systems needed for endurance events.')
    st.divider()

    st.write('***Your M (marathon running) pace is:***')
    # (int(m_mile/60)) takes integer part of answer (i.e. rounds down) and (m_mile % 60) is modulo function for remainder
    st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % (int(m_mile/60)) +' minutes and ' + "%.0f" % (m_mile % 60) + ' seconds per mile</strong></em></span>', unsafe_allow_html=True)
    st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % (int(m_km/60)) +' minutes and ' + "%.0f" % (m_km % 60) + ' seconds per km</strong></em></span>', unsafe_allow_html=True)
    st.write('Experienced distance athletes can maintain this intensity for several hours so it\'s your marathon running pace. In terms of training stress, it\'s about twice as hard as your easy training zone so do about 25% of your training in this zone.')
    st.divider()

    st.write('***Your T (lactate threshold) pace is:***')
    st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % (int(t_mile/60)) +' minutes and ' + "%.0f" % (t_mile % 60) + ' seconds per mile</strong></em></span>', unsafe_allow_html=True)
    st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % (int(t_km/60)) +' minutes and ' + "%.0f" % (t_km % 60) + ' seconds per km</strong></em></span>', unsafe_allow_html=True)
    st.write('Lactate threshold intensity. Improves speed endurance (your ability to hang on to a hard pace). Aim for about 10% of your weekly mileage or up to an hour a week at this intensity.')
    st.divider()
    
    # Everyone has a 400m I time (and it's always >60 seconds) but not necessarily a km or mile time
    st.write('***Your I (interval run) pace is:***')
    if i_mile > 0:  
        st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % (int(i_mile/60)) +' minutes and ' + "%.0f" % (i_mile % 60) + ' seconds per mile</strong></em></span>', unsafe_allow_html=True)
    if i_km > 0:
        st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % (int(i_km/60)) +' minutes and ' + "%.0f" % (i_km % 60) + ' seconds per km</strong></em></span>', unsafe_allow_html=True)
    st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % (int(i_400/60)) +' minutes and ' + "%.0f" % (i_400 % 60) + ' seconds per 400m</strong></em></span>', unsafe_allow_html=True)
    st.write('Speed work to improve your VO\u2082max. Repeated work intervals of up to 5 minutes each with easy zone recoveries of similar duration. Hard physically and mentally so aim for no more than 8% of your weekly mileage in this zone. Or if you are happy with the pace you run at already and just want to go further, skip them completely.')
    st.divider()

    # Everyone has a 200m and 400m R time but not necessarily an 800m time
    # But the 200m & 400m times aren't necessarily > 1 minute
    st.write('***Your R (repetition run) pace is:***')
    if r_800 > 0:  
        st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % (int(r_800/60)) +' minutes and ' + "%.0f" % (r_800 % 60) + ' seconds per 800m</strong></em></span>', unsafe_allow_html=True)  
    if r_400 > 59:
        st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % (int(r_400/60)) +' minutes and ' + "%.0f" % (r_400 % 60) + ' seconds per 400m</strong></em></span>', unsafe_allow_html=True)
    else:
        st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % r_400 + ' seconds per 400m</strong></em></span>', unsafe_allow_html=True)
    if r_200 > 59:
        st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % (int(r_200/60)) +' minutes and ' + "%.0f" % (r_200 % 60) + ' seconds per 200m</strong></em></span>', unsafe_allow_html=True)
    else:
        st.write('&emsp;<span style="color:#F63366;"><em><strong>' + "%.0f" % r_200 + ' seconds per 200m</strong></em></span>', unsafe_allow_html=True)
    st.write('Speed work to develop running economy and power. Repeated work efforts of up to 2 minutes each with full recoveries in between. Up to about 5% of your weekly mileage')      
    st.divider()

with st.expander('Would you like to see your potential race finish times?'):
    # Won't find a value if 'trigger' is still at default value of 29 and throw an exception so only enter if the value has been changed by user input
    if trigger>29:
        _1500m = lookup_table.loc[lookup_table['VDOT'] == trigger, '1500m'].item()
        _5k = lookup_table.loc[lookup_table['VDOT'] == trigger, '5000m'].item()
        _10k = lookup_table.loc[lookup_table['VDOT'] == trigger, '10,000m'].item()
        _10k_hrs = (int(_10k/3600))
        half_marathon = lookup_table.loc[lookup_table['VDOT'] == trigger, 'Half marathon'].item()
        half_marathon_hrs = (int(half_marathon/3600))
        marathon = lookup_table.loc[lookup_table['VDOT'] == trigger, 'Marathon'].item()
        marathon_hrs = (int(marathon/3600))

        st.write('With enough E and M pace training to allow you to comfortably cover the distance, your aerobic fitness is high enough that you have the potential to run:')
        st.write('&emsp;<em><strong>A 1500m race in <span style="color:#F63366;">' + "%.0f" % (int(_1500m/60)) + ' minutes and ' + "%.0f" % (_1500m % 60) + ' seconds</span></strong></em>', unsafe_allow_html=True)
        st.write('&emsp;<em><strong>A 5km race in <span style="color:#F63366;">' + "%.0f" % (int(_5k/60)) + ' minutes and ' + "%.0f" % (_5k % 60) + ' seconds</span></strong></em>', unsafe_allow_html=True)
        if _10k_hrs > 0:
            st.write('&emsp;<em><strong>A 10km race in<span style="color:#F63366;"> 1 hour, ' + "%.0f" % (int((_10k-3600)/60)) + ' minutes and ' + "%.0f" % ((_10k-3600) % 60) + ' seconds</span></strong></em>', unsafe_allow_html=True)
        else:
            st.write('&emsp;<em><strong>A 10km race in <span style="color:#F63366;">' + "%.0f" % (int(_10k/60)) + ' minutes and ' + "%.0f" % (_10k % 60) + ' seconds</span></strong></em>', unsafe_allow_html=True)   
        if half_marathon_hrs > 1:
            st.write('&emsp;<em><strong>A half marathon race in <span style="color:#F63366;">' + "%.0f" % half_marathon_hrs + ' hours, '  + "%.0f" % (int((half_marathon-3600*half_marathon_hrs)/60)) + ' minutes and ' + "%.0f" % ((half_marathon-3600*half_marathon_hrs) % 60) + ' seconds</span></strong></em>', unsafe_allow_html=True)
        elif half_marathon_hrs == 1:
            st.write('&emsp;<em><strong>A half marathon race in <span style="color:#F63366;">1 hour, ' + "%.0f" % (int((half_marathon-3600*half_marathon_hrs)/60)) + ' minutes and ' + "%.0f" % ((half_marathon-3600*half_marathon_hrs) % 60) + ' seconds</span></strong></em>', unsafe_allow_html=True)
        else:
            st.write('&emsp;<em><strong>A half marathon race in <span style="color:#F63366;">' + "%.0f" % (int(half_marathon/60)) + ' minutes and ' + "%.0f" % ((half_marathon) % 60) + ' seconds</span></strong></em>', unsafe_allow_html=True)
        st.write('&emsp;<em><strong>A marathon race in <span style="color:#F63366;">' + "%.0f" % marathon_hrs + ' hours, '  + "%.0f" % (int((marathon-3600*marathon_hrs)/60)) + ' minutes and ' + "%.0f" % ((marathon-3600*marathon_hrs) % 60) + ' seconds</span></strong></em>', unsafe_allow_html=True)  
        st.write('\n')
        st.write('If you want race one of these distances faster than that, you\'ll have to increase your VDOT by introducing some interval and repetition running into your training schedule. Expand the Notes section below for some suggestions on how to do this.')     




st.write('\n')
st.write('\n')
donate_left, donate_right = st.columns([1, 3])
with donate_left:
    st.write('\n')
    st.markdown(donate_text, unsafe_allow_html=True)

with donate_right:
    st.write('\n')
    redirect_button("https://www.paypal.com/donate/?hosted_button_id=6X8E9CL75SRC2")   

st.write('\n')
st.write('\n')
#notes = st.button('Notes:small_red_triangle_down:')
with st.expander('Notes'):
    st.markdown('The training pace calculations shown here are based on the methods of legendary running coach and exercise physiologist [Jack Daniels](https://en.wikipedia.org/wiki/Jack_Daniels_(coach)). His work training runners of all standards for decades has established three important principles:<ul><li>You can accurately predict someone\'s finishing time at one race distance from their finishing time at a different race distance</li><li>That someone\'s running performance is directly related to a measure known as their VDOT, the product of their ability to absorb oxygen from the air and get it to their running muscles (their VO\u2082max) and their running style efficiency (i.e. how efficiently they use that oxygen to propel themselves forwards)</li><li>Someone\'s race performances and VDOT can be used to determine a range of different training paces that can be used to enable them to run further, run faster or hold on to a pace for longer</li></ul>This was published by Jack in a number of books including [Daniels\' Running Formula](https://www.waterstones.com/book/daniels-running-formula/jack-daniels/9780736054928) and online resources. This app distills those decades of work and published tables and does the calculations for you.<br>If you start off an exercise gently and gradually build the intensity up, at first you have enough oxygen available to perform the exercise entirely aerobically. As the intensity builds, you reach a point where your body can\'t supply oxygen fast enough any more, you start to go deeply anaerobic and rapidly build up lactate in your blood. This point is called your \'lactate threshold\'. The combination of the inefficiency of anaerobic metabolism, the pain that comes from lactate build up in your muscles (\'muscle pump\') and the uncomfortableness of the very heavy breathing that comes with it means you can\'t keep up anaerobic exercise for long whereas even moderately trained people can keep entirely aerobic activity up for several hours.<br>In terms of training paces, your E (easy) and M (marathon) training paces calculated above are almost entirely aerobic. This is where you teach your body to burn fat as a fuel so you can go long without hitting the wall. E pace gets you most of the benefits of endurance training: it\'s intense enough to bring a training effect without stressing your body so hard you can\'t get out the next day. Your heart reaches its maximum stroke volume in this zone as well so it\'s the easiest way to get the benefits of a healthy heart. The M (marathon) training pace is about the intensity you\'d race at in an event lasting several hours (i.e. it\'s marathon running pace). It gets you used to judging that pace, feeding on the move and can be used to break up a bit of the tedium of plodding along at E pace. The one thing you won\'t get from training exclusively in these zones is much faster: you\'ll tend to go longer, more comfortably and be less injury prone but if you want to go faster you\'ll want to start putting some anaerobic work into your schedule.<br>T pace is threshold intensity. Threshold is that point at which your body is beginning to struggle to flow oxygen to your muscles fast enough. Training at this pace builds your speed endurance: your ability to hang on to a pace. If you only have time for a couple of 20 minute runs a week, doing them at T pace will probably get you the most return for your time. For athletes with bigger training schedules, aim for about 10% of your training time in this zone. You are burning glycogen almost exclusively at this intensity and because your body doesn\'t have much of it, most people can\'t keep this intensity up for more than an hour (for runners it roughly corresponds to your 10km race pace). Try either doing your T pace work as one long session or do it as, say, 15 minute bursts interspersed with easy zone work: mix it up, keep it interesting.<br>I (interval) and R (repetition) paces are more deeply anaerobic; it\'s where you are overstressing the ability of your heart, lungs, vascular system and mitochondria to supply oxygen to your muscles. You are burning entirely glycogen at these intensities and doing it increasingly inefficiently resulting in lactate build up in your blood which is what makes training at these intensities so hard. Intervals are repeated runs of between 3 and 5 minutes duration done at I pace with similar time recovery periods (done at E pace or walking). Repetitions are more for developing top speed and running efficiency. These are repeated runs of about 30 seconds to a minute duration at R pace with full recoveries in between (about 4 times the R duration done at E pace). Training in these zones should make you faster, stronger and improve your VO\u2082max (maximum rate at which you can flow oxygen to your muscles) and running efficiency. But it won\'t do much to improve your chance of completing a marathon because you don\'t have enough glycogen to cover these distances, and that\'s the only fuel you are using at I and R pace. It\'s also tough mentally and physically which is why the 8% and 5% of your weekly mileage recommendations are there.<br>In this app, you can use a recent race time to estimate your VDOT and appropriate training paces. You can enter a known VDOT on the slider if you have one. If you don\'t have a recent race time or know your VDOT (e.g. if you are new to running) don\'t worry: you can get a very good estimate of your VDOT [by performing a beep test using this app](https://beep-test.streamlit.app/) and using the calculated VO\u2082max as the input to the VDOT on the slider in this app (they aren\'t quite the same thing but it\'ll be close enough).<br>Finally, if you are running primarily for weight loss, a few observations. (It varies a bit depending on your size but) generally no matter how fast you run, you\'re burning about 100 calories a mile. This is about the number of calories in one biscuit. There are about 3700kcal in 1lb (0.45kg) of adipose tissue (\'body fat\'). From this you can work out that you need to run a lot of miles to lose much weight unless you accompany it with diet and lifestyle changes. Men\'s Health style articles will often tell you that high intensity interval training (I and R pace running) burns more calories and raises your metabolism more than plodding along at easy pace so is better for weight loss. There\'s some truth in this and it\'s seductive because everyone likes the idea of more for less. But hand in hand with that is the fact that because the efforts are so hard you can manage fewer of them per session interspersed with relatively long rest periods. When you work it all out, no matter what style of running training you do, most people are using between about 600 and 800 calories an hour. Don\'t expect to lose much weight if you do two 20 minute runs a week and wash them down with a Big Mac.<br><small>*Comments, queries or suggestions? [Contact us](https://www.elephant-stone.com/contact.html)*.</small>', unsafe_allow_html=True)
    

