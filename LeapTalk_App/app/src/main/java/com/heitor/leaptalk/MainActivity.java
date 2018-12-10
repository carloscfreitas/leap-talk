package com.heitor.leaptalk;

import com.google.android.glass.media.Sounds;
import com.google.android.glass.widget.CardBuilder;
import com.google.android.glass.widget.CardScrollAdapter;
import com.google.android.glass.widget.CardScrollView;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.media.AudioManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;


public class MainActivity extends Activity {


    private static final int SERVERPORT = 34000;
    private static final String SERVER_IP = "192.168.1.12";
    private static String rcv = "";



    protected void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        setContentView(R.layout.main);


        new AsyncThread().execute();

        final TextView screen = (TextView)findViewById(R.id.screen);

        new CountDownTimer(Long.MAX_VALUE, 1000) {
            private int sec = 0;
            public void onTick(long millisUntilFinished) {
                screen.setText(rcv);
                this.sec++;
            }

            @Override
            public void onFinish() {}
        }.start();

    }

    @Override
    protected void onResume() {
        super.onResume();

    }

    @Override
    protected void onPause() {
        super.onPause();
    }

    public class AsyncThread extends AsyncTask<String, String, String>
    {

        //High priority UI variables goes below....
        private PrintStream out;
        private Socket socket;
        private BufferedReader in;

        //Least priority variables goes below.....
        private final String TAG = "AsyncThread";

        @Override
        protected String doInBackground(String... params) {

            final TextView screen = (TextView)findViewById(R.id.screen);

            StringBuilder buffer = null;

            try {
                socket = new Socket(SERVER_IP, SERVERPORT);

                /////////////---------CODE TO READ & WRITE------------\\\\\\\\\\\\\\\\\\\\\\\\\

                final BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    while(true) {
                        while (input.ready() == false) {
                            Log.e("DEBUUUG", input.readLine());
                            rcv = input.readLine();
                        }
                    }

            }//TRY closes here....
            catch(Exception e){
                e.printStackTrace();
            }//catch closes here.....

            return "nada";
        }//doInBackground CLOSES HERE.....
    }//AsyncThread class closes here.....
}