# Create Frequency Overtones with Python  

A small walkthrough on how to generate musical overtones with the Karplus-Strong algorithm.  

*Adapted from Python Playground, by Mahesh Venkitachalam.*  

## Introduction 

In this project, you'll generate five guitar-like notes of a musical scale (series of related notes) using the Karplus-Strong Algorithm. You'll visualize the algorithm used to generate these notes and save the sounds as WAV files. You'll also create a way to play them at random and learn how to do the following:  

* Implement a ring buffer using the Python `deque` class  
* Use `numpy` arrays and `ufuncs`  
* Play WAV files using `pygame`  
* Plot a graph using `matplotlib`  
* Play the pentatonic musical scale  

In addition to implementing the Karplus-Strong algorithm in Python, you'll also explore the WAV file format and see how to generate notes within a pentatonic musical scale.       

One of the characteristics of any musical sound is its pitch, or **frequency**. This is the number of vibrations per second in hertz (Hz). For example, the third string from the top of an acoustic guitar produces a D note, which has a frequency of 146.83 Hz. You can approximate this sound by creating a sine wave with the same vibrations per second on a computer.  

The dominant frequency you hear when you pluck the D string on a guitar, called the **fundamental frequency**, is the 146.83 Hz, but you also hear certain multiples of that frequency called **overtones**. This is true for any instrument, it is comprised of a fundamental frequency and overtones; it's the combination of these two that makes a flute sound like a flute, a guitar sound like a guitar, etc.  

So to simulate the sound of a plucked guitar string instrument on the computer, you need to be able to generate both the fundamental frequency and the overtones. To do this, we can use the **Karplus-Strong** algorithm.  

## How it Works  

The Karplus-Strong algorithm can simulate the sound of a plucked string by using a **ring buffer** of displacement values to simulate a string tied down at both ends, similar to a guitar string. Also known as a *circular buffer*, a ring buffer is a fixed-length (simply an array of values) that wraps around itself. In other words, when you reach the end of a buffer, the next element you access will be the first element in the buffer.  

The length (N) of the ring buffer is related to the fundamental frequency of vibration according to the equation N =S/*f*, where S is the sampling rate and *f* is the frequency.  

In the beginning of the simulation, the buffer is filled with random values in the ragne [-0.5, 0.5]. Think of this as the representation of the random displacement of a plucked string as it vibrates.

We'll use a **samples buffer** to store the intensity of the sound at any certain time. The length of this buffer and the sampling rate determine the length of the sound clip.  

### The Simulation  

The simulation proceeds until the sample buffer is loaded up in a feedback-style. Think of the samples buffer as a list: [t0, t1, t2, t3...]. To simulate a plucked string, fill a ring buffer with numbers that represent the energy of the wave. The sample buffer, which represents the final sound data, is created by iterating through the ring buffer values. We'll use an **averaging scheme** to update values in the ring ubffer.

You would do the following for each step of the simulation:  

1. Store the value from the ring buffer in the samples buffer.  
2. Calculate the average of the first two elements in the ring buffer.  
3. Multiply this average value by an attenuation factor.  
4. Add (or append) this value to the end of the ring buffer.  
5. Remove the first element of the ring buffer.  

This feedback-style format is designed to simulate the traveling energy through a string that is vibrating.  

The length of a vibrating string is inversely proportional to the fundamental frequency -physics. Because we want to create sounds of a particular frequency, we'll choose a ring buffer length that is inversely proportional to that frequency.  

In step 1, above, the averaging that happens acts as the *low-pass filter* that cuts off higher frequencies and allows lower frequencies through, which eleminates higher *harmonics* (larger multiples of the fundamental frequency) because we only want the fundamental frequency. Finally, we'll use the attentuation factor to simulate the loss of energy as the wave moves back and forth along the string. This sample buffer we use in step 1 represents the amplitude of the created sound over time. To calculate the amplitude at any time, just update the ring buffer by calculating the average of its first two elements and multiply that result by an attenuation factor. The result is then added (or appended) to the end of the ring buffer, and the first element of the ring buffer is removed.  

### Creating WAV Files  

The *Waveform Audio File Format (WAV)* is used to store audio data. This format is convienent for small audio projects, for it is simple and you do  not need to deal with complex compression techniques.  

WAV files consist of a series of bits representing the amplitude of the recorded sound at a given point in time, a.k.a **resolution**. A **sampleing rate** is the number of times the audio is read, *or sampled*, every second. For our project, we will use a sampling rate of 44,100 Hz, the same rate used in audio compact discs (CDs).  

To generate a five-second audio clip of a 220 Hz in Python, you will use a formula to represent a sine wave:

<center>  

A = sin(2π*ft*)  

</center>  

Where A is the amplitude of the wave, *f* is the frequency, and *t* is the current time index. Let's rewrite the formula to fir our needs:  

<center>  

A = sin(2π*fi*/*R*)

</center>  

*i* is the index of the sample, *R* is the sampling rate.  

Using these two equations, we can create a WAV file for a 200 Hz sine wave.  

### Create a 5-Sec WAV file for a 200 Hz Sine Wave Using Python  

Create a new Python file called, my_sine_wave.py  

```python  
import numpy as np
import wave, math

sRate = 44100
nSamples = sRate * 5

# Create a numpy array of amplitude values via the second sine wave equation:
x = np.arange(nSamples)/float(sRate)
vals = np.sin(2.0*math.pi*220.0*x)

# So we can write to a file, the computed sine wave values in the range [-1, 1] are
# scaled to 16-bit values and converted to a string:
data = np.array(vals*32767, 'int16').tostring()
file = wave.open('sine220.wav', 'wb')

# Set the parameters of the WAAV file:
file.setparams((1, 2, sRate, nSamples, 'NONE', 'uncompressed'))

# Write to the file using the parameters above:
file.writeframes(data)

# Close the file
file.close()
```  

After executing the program, a WAV file is created. Play the file to hear the sound! You will hear a 220 Hz tone for five seconds.  

<center>  

![220hz sine wave](images/sine_wave_220hz.jpg)  

</center>  

Above shows the WAV file we generated in a free audio editor, Audacity. As we expect, we can see a sine wave frequency of 220 Hz. 

### The Minor Pentatonic Scale  

The **musical scale** is a series of notes in increasing or decreasing pitch or frequency. A **musical interval** is the difference between two pitches. Usually, all notes in a piece of music are chosen from a particular scale. A **semitone** is a basic building block of a scale and is the smallest musical interval in *western* music. A **tone** is twice the length of a semitone. The **major scale**, one of the most common musical scales, is defined by the interval pattern *tone-tone-semitone-tone-tone-tone-semitone*.  

## The Main Project  
In this project, we'll use our friend, Python and its `wave` module to create audio files in the WAV format. We'll also use `numpy` arrays for the Karplus-Strong algorithm and the `deque` class from Python collections to implement the famous ring buffer. Finally, we will play back the WAV files using `pygame`.  

We'll go over each part, then put it all together for a finished product.  

<center>  

![simulate pluck](images/plucked_string_simulation.jpg)
</center>  




