import edu.cmu.ri.createlab.hummingbird.HummingbirdRobot;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class ClassTemplate {

    public static void main(String[] args) throws IOException, InterruptedException {

        HummingbirdRobot YourRobotNameHere = new HummingbirdRobot();

        System.out.println("");
        System.out.println("**********PROGRAM START************");
        System.out.println("");
               
        YourRobotNameHere.setLED(1,253);
        Thread.sleep(1000);
        YourRobotNameHere.setLED(1,0);
        Thread.sleep(1000);
        YourRobotNameHere.setLED(1,253);
        Thread.sleep(1000);
		System.out.println(YourRobotNameHere.getSensorValue(1));
		YourRobotNameHere.setMotorVelocity(1, 255);
		YourRobotNameHere.setServoPosition(1, 230);
        Thread.sleep(2000);
        YourRobotNameHere.setServoPosition(1, 0);
        Thread.sleep(1000);
        YourRobotNameHere.disconnect();
        

        System.out.println("");
        System.out.println("**********PROGRAM END************");
        System.out.println("");
    }
}
